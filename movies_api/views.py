from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *

class GenomeTagsAPI(viewsets.ModelViewSet):
    serializer_class = GenomeTagsSerializer
    queryset = GenomeTags.objects.all()[:5]


class LinksAPI(viewsets.ModelViewSet):
    serializer_class = LinksSerializer
    queryset = Links.objects.all()[:5]


class MoviesAPI(viewsets.ModelViewSet):
    serializer_class = MoviesSerializer
    queryset = Movies.objects.all()[:5]

class RatingsAPI(viewsets.ModelViewSet):
    serializer_class = RatingsSerializer
    queryset = Ratings.objects.all()[:5]


class TagsAPI(viewsets.ModelViewSet):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()[:5]

class UsersAPI(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = Users.objects.all()[:5]