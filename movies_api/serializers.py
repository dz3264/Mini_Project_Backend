from rest_framework import serializers
from .models import *

class LinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = "__all__"

class RatingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = "__all__"

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = "__all__"

class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = "__all__"

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"


