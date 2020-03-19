from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Links)
admin.site.register(models.Movies)
admin.site.register(models.Ratings)
admin.site.register(models.Tags)
admin.site.register(models.Users)
