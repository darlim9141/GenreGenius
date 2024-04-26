from django.db import models


class FavoriteMusic(models.Model):
    song1 = models.CharField(max_length=100)
    song2 = models.CharField(max_length=100)
    song3 = models.CharField(max_length=100)