from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('movies/', MoviesAPI),
    path('movie/<movieid>', MovieDetailAPI, name="details"),
    path('rating/<movieid>', RatingAPI, name="movie_ratings"),
    path('ratingby/<userid>', RatingByAPI, name="user_ratings"),
]