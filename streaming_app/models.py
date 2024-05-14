from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    omdb_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    genres = models.ManyToManyField(Genre)
    type = models.CharField(max_length=255, default='movie')
    poster = models.URLField(default="https://downtownwinnipegbiz.com/wp-content/uploads/2020/02/placeholder-image.jpg")

    def __str__(self):
        return self.title
