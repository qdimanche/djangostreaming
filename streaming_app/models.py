from django.db import models


class Movie(models.Model):
    omdb_id = models.CharField(max_length=50, unique=True, default='')
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    type = models.CharField(max_length=255)
    poster = models.URLField()

    def __str__(self):
        return self.title
