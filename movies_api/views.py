from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *

DEFAULT_LIMIT = 100

@api_view(['GET'])
def MoviesAPI(request):

    if request.method == 'GET':

        # Get query params
        year_from = request.GET.get('from')+"-01-01" if request.GET.get('from') else '1900-01-01'
        year_to = request.GET.get('to')+"-01-01" if request.GET.get('to') else '2100-01-01'
        limit = int(request.GET.get('limit')) if request.GET.get('limit') else DEFAULT_LIMIT
        sort = '-'+request.GET.get('sort') if request.GET.get('sort') else '-movieid'
        page = int(request.GET.get('page')) if request.GET.get('page') else 1

        if year_to and year_from:
            movies = Movies.objects.filter(release_date__range=(year_from, year_to)).order_by(sort)
        else:
            movies = Movies.objects.all().order_by(sort)

        start = (page-1)*limit
        end = page*limit

        serializer = MoviesSerializer(movies[start:end], many=True)

        return Response({'total_count': len(movies),'current_count':len(serializer.data), 'data': serializer.data})

@api_view(['GET'])
def MovieDetailAPI(request, movieid):

    try:
        movie = Movies.objects.get(movieid=movieid)

    except Movies.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MoviesSerializer(movie)

        return Response({'data':serializer.data})

@api_view(['GET'])
def RatingAPI(request, movieid):

    if request.method == 'GET':

        # if need details of ratings
        detail = True if request.GET.get('detail') else False
        try:
            ratings = Ratings.objects.filter(movieid=movieid)
            serializer = RatingsSerializer(ratings, many=True)

            if not detail:
                ratings_list = list(serializer.data)
                ratings_count = {0:0, 0.5:0, 1:0, 1.5:0, 2:0, 2.5:0, 3:0, 3.5:0, 4:0, 4.5:0, 5:0}
                for r in ratings_list:
                    ratings_count[r['rating']] += 1

        except Ratings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response({'total_count':len(serializer.data), 'detail':detail,'data':serializer.data if detail else ratings_count})

@api_view(['GET'])
def RatingByAPI(request, userid):
    try:
        ratings = Ratings.objects.filter(userid=userid)

    except Ratings.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RatingsSerializer(ratings, many=True)

        return Response({'total_count':len(serializer.data),'data':serializer.data})


# https://docs.djangoproject.com/en/3.0/topics/db/queries/

