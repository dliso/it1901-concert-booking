from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

MAX_CHARFIELD_LENGTH_GENERAL = 200
MAX_BANDNAME_LENGTH = MAX_CHARFIELD_LENGTH_GENERAL
MAX_STAGENAME_LENGTH = MAX_CHARFIELD_LENGTH_GENERAL


class Band(models.Model):
    name = models.CharField(max_length=MAX_BANDNAME_LENGTH)
    manager = models.ForeignKey(User, null=True, blank=True)

    # This model has to be expanded to include at least genres.

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name + " - " + self.description


class Stage(models.Model):
    name = models.CharField(max_length=MAX_STAGENAME_LENGTH)


class Concert(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)
    unique_for_date = "pub_date"
    band_name = models.ForeignKey(Band)
    stage_name = models.ForeignKey(Stage)
    genre_music = models.ForeignKey(Genre)
    #created_time = models.DateTimeField(default=timezone.now, editable=False) #time concert object created
    concert_time = models.DateTimeField(blank=True, null=True) #time concert happening
    concert_description = models.TextField(blank=True)

    def __str__(self):
        return self.name + " - " + self.concert_description

    # This model has to be expanded to include which bands are playing, what
    # stage it's happening on, technical requirements, who's performing
    # technical duties.
