# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class GenomeTags(models.Model):
    tagid = models.IntegerField(db_column='tagId', primary_key=True)  # Field name made lowercase.
    tag = models.TextField()

    class Meta:
        managed = False
        db_table = 'genome-tags'


class Links(models.Model):
    movieid = models.IntegerField(db_column='movieId', primary_key=True)  # Field name made lowercase.
    imdbid = models.CharField(db_column='imdbId', max_length=50)  # Field name made lowercase.
    tmdbid = models.CharField(db_column='tmdbId', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'links'


class Movies(models.Model):
    movieid = models.IntegerField(db_column='movieId', primary_key=True)  # Field name made lowercase.
    title = models.TextField()
    genres = models.TextField(blank=True, null=True)
    tmdb = models.IntegerField(blank=True, null=True)
    popularity = models.FloatField(blank=True, null=True)
    original_language = models.TextField(blank=True, null=True)
    production_countries = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    revenue = models.IntegerField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    adult = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'


class Ratings(models.Model):
    userid = models.IntegerField(db_column='userId')  # Field name made lowercase.
    movieid = models.IntegerField(db_column='movieId')  # Field name made lowercase.
    rating = models.FloatField(blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratings'


class Tags(models.Model):
    userid = models.ForeignKey('Users', models.DO_NOTHING, db_column='userId')  # Field name made lowercase.
    movieid = models.IntegerField(db_column='movieId')  # Field name made lowercase.
    tag = models.TextField(blank=True, null=True)
    timestamp = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tags'


class Users(models.Model):
    userid = models.IntegerField(db_column='userId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=45)  # Field name made lowercase.
    userpass = models.CharField(db_column='userPass', max_length=45)  # Field name made lowercase.
    userhistory = models.TextField(db_column='userHistory', blank=True, null=True)  # Field name made lowercase.
    usertags = models.TextField(db_column='userTags', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'users'
