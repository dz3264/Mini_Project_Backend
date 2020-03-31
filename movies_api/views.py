from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg
from django.db import connection
import numpy as np
from .serializers import *
from .models import *
from .movie_rec_website.example_norating import make_norating_rec
from .movie_rec_website.example2 import make_rec

import heapq
import time

DEFAULT_LIMIT = 60
REC_LIM = 20
CAPACITY = 20
ALL_GENRES = ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy',
              'Romance', 'Drama', 'Action', 'Crime', 'Thriller',
              'Horror', 'Mystery', 'Sci-Fi', 'IMAX', 'Documentary',
              'War', 'Musical', 'Western', 'Film-Noir']

@api_view(['GET'])
def RecommandAPI(request, userid):


    if request.method == 'GET':

        cursor = connection.cursor()

        # recommand by rating
        cursor.execute('''SELECT * FROM ratings left join movies 
        ON ratings.movieId = movies.movieId 
        WHERE ratings.userId = %s ORDER BY -timestamp LIMIT %s;''',[userid,REC_LIM])
        rows = cursor.fetchall()
        newmovieId = [ r[5] for r in rows]
        newrating =[ r[3] for r in rows]

        if(len(newmovieId) == 0):
            rec_rating_id = []
        else:
            rec_rating_id = make_rec(newmovieId, newrating)

        # recommand by history
        try:
            user = Users.objects.get(userid=userid)
            if not user.userhistory:
                rec_history_id = []

            else:
                # userhistory only keep 20
                newmovieId = [int(m) for m in user.userhistory.keys()]
                rec_history_id = make_norating_rec(newmovieId)


        except Users.DoesNotExist:
            rec_history_id = []

        rec_movies_id = set(list(rec_rating_id) + list(rec_history_id))
        #print(rec_movies_id)
        rec_movies = []

        for rec in rec_movies_id:
            try:
                movie = Movies.objects.get(movieid=rec)

            except Movies.DoesNotExist:
                continue

            movie_serializer = MoviesSerializer(movie)
            rec_movies.append(movie_serializer.data)


        return Response({'rec_movies':rec_movies},status=status.HTTP_200_OK)


@api_view(['GET'])
def MoviesAPI(request):

    if request.method == 'GET':

        # Get query params
        year_from = request.GET.get(
            'from')+"-01-01" if request.GET.get('from') else '1800-01-01'
        year_to = request.GET.get(
            'to')+"-01-01" if request.GET.get('to') else '2100-01-01'
        limit = int(request.GET.get('limit')) if request.GET.get(
            'limit') else DEFAULT_LIMIT
        sort = request.GET.get('sort') if request.GET.get(
            'sort') else 'movieid'
        page = int(request.GET.get('page')) if request.GET.get('page') else 1
        genre = request.GET.get('genre') if request.GET.get('genre') else ''
        key = request.GET.get('key') if request.GET.get('key') else ''

        # the first several pages already have some movies from recommendation
        offset = int(request.GET.get('offset')) if request.GET.get('offset') else 0

        movies = Movies.objects.filter(release_date__range=(
            year_from, year_to)).filter(genres__contains=genre).filter(title__contains=key).order_by(sort)

        if not movies:
            movies = Movies.objects.filter(title__contains=key).order_by(sort)


        if(page == 1):
            start = 0
            end = limit-offset
        else:
            start = (limit-offset)+(page-2)*limit
            end = (limit-offset)+(page-1)*limit

        serializer = MoviesSerializer(movies[start:end], many=True)

        return Response({'total_count': len(movies),
                         'current_count': len(serializer.data),
                         'data': serializer.data})


@api_view(['GET'])
def MovieGenres(request, genre):
    # print(genre)
    query_from = int(request.GET.get('from')
                     ) if request.GET.get('from') else 1800
    query_to = int(request.GET.get('to')) if request.GET.get('to') else 2100
    movies = {}

    if genre == 'All':
        for g in ALL_GENRES:
            year_from = str(query_from) + "-01-01"
            year_to = str(query_to) + "-01-01"
            movies[g] = Movies.objects.filter(release_date__range=(
                year_from, year_to)).filter(genres__contains=g).count()

    elif genre == 'Rating':
        query_genre = request.GET.get(
            'genre') if request.GET.get('genre') else ''
        year_from = str(query_from) + "-01-01"
        year_to = str(query_to) + "-01-01"
        movies_data = Movies.objects.filter(release_date__range=(
            year_from, year_to)).filter(genres__contains=query_genre)

        serializer = MoviesSerializer(movies_data, many=True)
        movies = {'0-2': 0, '2-4': 0, '4-6': 0, '6-8': 0, '8-10': 0}

        for m in list(serializer.data):
            average = float(m['vote_average'])
            # print(average)
            try:
                if int(m['vote_count']) < 1:
                    continue

                if average < 2:
                    movies['0-2'] += 1
                elif average < 4:
                    movies['2-4'] += 1
                elif average < 6:
                    movies['4-6'] += 1
                elif average < 8:
                    movies['6-8'] += 1
                else:
                    movies['8-10'] += 1
            except:
                continue

    else:
        for y in range(int(query_from), int(query_to)):
            year_from = str(y) + "-01-01"
            year_to = str(y+1) + "-01-01"
            movies[y] = Movies.objects.filter(release_date__range=(
                year_from, year_to)).filter(genres__contains=genre).count()

    return Response({'genre': genre, 'movies': movies, 'year_range': (query_from, query_to)})


@api_view(['GET'])
def MovieDetailAPI(request, movieid):

    try:
        movie = Movies.objects.get(movieid=movieid)

    except Movies.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MoviesSerializer(movie)

        return Response({'data': serializer.data})


@api_view(['GET'])
def RatingAPI(request, movieid):

    if request.method == 'GET':

        start = time.time()

        # if need details of ratings
        detail = True if request.GET.get('detail') else False
        limit = int(request.GET.get('limit')) if request.GET.get('limit') else DEFAULT_LIMIT
        sort = request.GET.get('sort') if request.GET.get('sort') else 'userid'
        movie = Movies.objects.get(movieid=movieid)
        movie_serializer = MoviesSerializer(movie)

        print('Set Up :', time.time()-start)


        try:
            start = time.time()

            ratings = Ratings.objects.filter(movieid=movieid).order_by(sort)
            #serializer = RatingsSerializer(ratings, many=True)

            print('Search data cost:', time.time() - start)

            #if not detail:
            start_AVG = time.time()
            average = ratings.aggregate(Avg('rating'))
            print('aggregate average cost', time.time() - start_AVG)
            #ratings_count = {0: 0, 0.5: 0, 1: 0, 1.5: 0,2: 0, 2.5: 0, 3: 0, 3.5: 0, 4: 0, 4.5: 0, 5: 0}
            #ratings_list = list(serializer.data)
            #for r in ratings_list: ratings_count[r['rating']] += 1

            """
            else:
                start = time.time()

                movies_ratings = []

                movie_rating = {
                    'movieId': movieid,
                    'movieTitle': movie_serializer.data['title'],
                    'userId':[],
                    'ratings':[],
                }
                userId = []
                ratings = []
                for r in serializer.data[:limit]:
                    userId.append(r['userid'])
                    ratings.append(r['rating'])

                movie_rating['userId'] = userId
                movie_rating['ratings'] = ratings

                movies_ratings.append(movie_rating)

                print('Listing data :', time.time() - start)
            """


        except Ratings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({'movieId': movieid,
                         #'movieTitle': movie_serializer.data['title'],
                         #'total_count': len(serializer.data),
                         'average': average['rating__avg'],
                         'detail': detail})
                         #'data': movies_ratings if detail else []})


@api_view(['GET','POST'])
def RatingByAPI(request, userid):

    if request.method == 'GET':

        movie = request.GET.get('movie') if request.GET.get('movie') else ''

        try:
            if movie:
                ratings = Ratings.objects.filter(userid=userid).filter(movieid=movie)

            else:
                ratings = Ratings.objects.filter(userid=userid)

        except Ratings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RatingsSerializer(ratings, many=True)

        return Response({'total_count': len(serializer.data), 'data': serializer.data})

    if request.method == 'POST':

        rating = Ratings.objects.filter(userid=request.data['userid'], movieid=request.data['movieid'])
        check = RatingsSerializer(rating, many=True)

        if not check.data:
            print('new rating')
            request.data['timestamp'] = int(time.time())
            serializer = RatingsSerializer(data=request.data)
            print(serializer)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'information':'Create New Rating',
                    'data':serializer.data}, status=status.HTTP_201_CREATED)

            else:
                print('serializer wrong')
                return Response('Invalid Serializer', status=status.HTTP_400_BAD_REQUEST)

        else:
            print('update rating')
            rating = Ratings.objects.get(userid=request.data['userid'], movieid=request.data['movieid'])
            rating.rating = request.data['rating']
            rating.timestamp = request.data['timestamp']
            rating.save()
        

            return Response({
                'information': 'Update Rating',
                'data':{
                "userid": rating.userid,
                "movieid": rating.movieid,
                "rating": rating.rating,
                "timestamp": rating.timestamp
            }}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def UserAPI(request, userid):

    if request.method == 'GET':

        try:
            user = Users.objects.filter(userid=userid)
            serializer = UsersSerializer(user, many=True)

            return Response({
                'data': {"userid": serializer.data[0]['userid'],
                         "username": serializer.data[0]['username'],
                         "userhistory": serializer.data[0]['userhistory'],
                         "usertags": serializer.data[0]['usertags']}})

        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



    if request.method == 'POST':

        try:
            user = Users.objects.get(userid=userid)

            if not user.userhistory :
                user.userhistory = {}

            movie = request.GET.get('movie') if request.GET.get('movie') else ''

            if movie:
                if movie in user.userhistory:
                    print('update')
                    user.userhistory[movie] = time.time()

                else:
                    print('new')
                    history = []
                    for key_m, value_t in user.userhistory.items():
                        history.append((value_t, key_m))

                    heapq.heapify(history)
                    print("history: ",history)

                    if len(history) >= CAPACITY:
                        # pop the smallest time which is oldest one
                        heapq.heappop(history)

                    heapq.heappush(history, (time.time(), movie))

                    user.userhistory = {}
                    for value_t, key_m in history:
                        user.userhistory[key_m] = value_t

            user.save()

            return Response(user.userhistory, status=status.HTTP_201_CREATED)

        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def Register(request):

    if request.method == 'POST':

        serializer = UsersSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def Login(request):

    if request.method == 'POST':


        try:
            user = Users.objects.filter(username=request.data['username'])
            serializer = UsersSerializer(user, many=True)
            print(serializer.data[0]['username'])

            if(serializer.data[0]['userpass'] != request.data['userpass']):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"userid": serializer.data[0]['userid'],
                             "username": serializer.data[0]['username'],
                             "userhistory": serializer.data[0]['userhistory'],
                             "usertags": serializer.data[0]['usertags']})

        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)





# https://docs.djangoproject.com/en/3.0/topics/db/queries/
