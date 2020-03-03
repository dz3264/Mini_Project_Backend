from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *


@api_view(['GET'])
def MoviesAPI(request):

    if request.method == 'GET':


        year_from = request.GET.get('from')
        year_to = request.GET.get('to')


        if year_to and year_from:
            movies = Movies.objects.filter(release_date__range = (year_from+"-01-01", year_to+"-12-31"))
        else:
            movies = Movies.objects.all()[:10]
        serializer = MoviesSerializer(movies, many=True)

        return Response(serializer.data)

# https://docs.djangoproject.com/en/3.0/topics/db/queries/

