from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('movies/', MoviesAPI),
    path('movie/<movieid>', MovieDetailAPI, name="details"),
    path('genres/<genre>', MovieGenres, name="movie_genre"),
    path('rating/<movieid>', RatingAPI, name="movie_ratings"),
    path('ratingby/<userid>', RatingByAPI, name="user_ratings"),
    path('user/<userid>', UserAPI, name="user"),
    path('register/', Register, name="register"),
    path('login/', Login, name="login"),
    path('rec/<userid>', RecommandAPI, name="recommand"),
]