from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Avg
from .serializers import *
from .models import *

DEFAULT_LIMIT = 50
ALL_GENRES = ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy',
              'Romance', 'Drama', 'Action', 'Crime', 'Thriller',
              'Horror', 'Mystery', 'Sci-Fi', 'IMAX', 'Documentary',
              'War', 'Musical', 'Western', 'Film-Noir']


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
        """
        'Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy', 
        'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 
        'Horror', 'Mystery', 'Sci-Fi', 'IMAX', 'Documentary', 
        'War', 'Musical', 'Western', 'Film-Noir', '(no genres listed)'
        """
        movies = Movies.objects.filter(release_date__range=(
            year_from, year_to)).filter(genres__contains=genre).order_by(sort)

        start = (page-1)*limit
        end = page*limit

        serializer = MoviesSerializer(movies[start:end], many=True)

        return Response({'total_count': len(movies), 'current_count': len(serializer.data), 'data': serializer.data})


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

        # if need details of ratings
        detail = True if request.GET.get('detail') else False
        try:
            ratings = Ratings.objects.filter(movieid=movieid)
            average = ratings.aggregate(Avg('rating'))
            serializer = RatingsSerializer(ratings, many=True)

            if not detail:
                ratings_list = list(serializer.data)
                ratings_count = {0: 0, 0.5: 0, 1: 0, 1.5: 0,
                                 2: 0, 2.5: 0, 3: 0, 3.5: 0, 4: 0, 4.5: 0, 5: 0}
                for r in ratings_list:
                    ratings_count[r['rating']] += 1

        except Ratings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({'total_count': len(serializer.data), 'average': average['rating__avg'], 'detail': detail, 'data': serializer.data if detail else ratings_count})


@api_view(['GET'])
def RatingByAPI(request, userid):
    try:
        ratings = Ratings.objects.filter(userid=userid)

    except Ratings.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RatingsSerializer(ratings, many=True)

        return Response({'total_count': len(serializer.data), 'data': serializer.data})


@api_view(['GET', 'POST'])
def UserAPI(request, userid):

    if request.method == 'GET':

        try:
            user = Users.objects.filter(userid=userid)
            serializer = UsersSerializer(user, many=True)
            return Response({'data': serializer.data})

        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':

        serializer = UsersSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# https://docs.djangoproject.com/en/3.0/topics/db/queries/
