from django.contrib.auth.models import User
from django.db import models

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


class Stage(models.Model):
    name = models.CharField(max_length=MAX_STAGENAME_LENGTH)


class Concert(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)

    # This model has to be expanded to include which bands are playing, what
    # stage it's happening on, technical requirements, who's performing
    # technical duties.
