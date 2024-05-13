from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=4)
    type = models.CharField(max_length=20)
    poster = models.URLField()

    def __str__(self):
        return self.title
