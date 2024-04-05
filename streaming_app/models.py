from django.db import models


# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=30)
    year = models.IntegerField(null=True, blank=True)
    genre = models.CharField(max_length=200)