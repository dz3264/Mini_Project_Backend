# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django_mysql.models import JSONField, Model


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


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
    release_date = models.TextField(blank=True, null=True)
    revenue = models.IntegerField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    adult = models.TextField(blank=True, null=True)
    vote_average = models.FloatField(blank=True, null=True)
    vote_count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movies'


class Ratings(models.Model):
    # Field name made lowercase.
    ratingid = models.AutoField(db_column='ratingId', primary_key=True)
    # Field name made lowercase.
    userid = models.IntegerField(db_column='userId')
    # Field name made lowercase.
    movieid = models.IntegerField(db_column='movieId')
    rating = models.FloatField()
    timestamp = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ratings'


class Tags(models.Model):
    userid = models.IntegerField(db_column='userId')  # Field name made lowercase.
    movieid = models.IntegerField(db_column='movieId')  # Field name made lowercase.
    tag = models.TextField()
    timestamp = models.IntegerField()
    tagid = models.AutoField(db_column='tagId', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tags'


class Users(models.Model):
    userid = models.AutoField(db_column='userId', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='userName', max_length=45)  # Field name made lowercase.
    userpass = models.CharField(db_column='userPass', max_length=45)  # Field name made lowercase.
    userhistory = JSONField(db_column='userHistory', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    usertags = JSONField(db_column='userTags', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'users'
