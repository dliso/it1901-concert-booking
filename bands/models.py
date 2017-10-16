from collections import namedtuple
from itertools import groupby

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

MAX_CHARFIELD_LENGTH_GENERAL = 200
MAX_BANDNAME_LENGTH = MAX_CHARFIELD_LENGTH_GENERAL
MAX_STAGENAME_LENGTH = MAX_CHARFIELD_LENGTH_GENERAL


class Band(models.Model):
    name = models.CharField(max_length=MAX_BANDNAME_LENGTH)
    manager = models.ForeignKey(User, null=True, blank=True)

    genre = models.ForeignKey('Genre', null=False, blank=False)
    sold_albums = models.PositiveIntegerField(default=0)
    total_streams = models.PositiveIntegerField(default=0)

    def previous_concerts(self):
        return Concert.objects.filter(
            concert_time__lt=timezone.now(),
            band_name=self
        ).order_by('-concert_time')

    def upcoming_concerts(self):
        return Concert.objects.filter(
            concert_time__gt=timezone.now(),
            band_name=self
        ).order_by('-concert_time')

    # This model has to be expanded to include at least genres.

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("band:detail",args=[self.id])

class TechnicalNeed(models.Model):
    concert_name = models.ForeignKey('Concert')
    sound = models.TextField(blank = True)
    light = models.TextField(blank = True)
    other_technical_needs = models.TextField(blank = True)

    def __str__(self):
        return self.concert_name.__str__()

    def get_absolute_url(self):
        return self.concert_name.get_absolute_url()

class Genre(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name + " - " + self.description


class Stage(models.Model):
    STAGE_SIZE_CHOICES = (('S','Small'),
                          ('M', 'Medium'),
                          ('L', 'Large'))

    name = models.CharField(max_length=MAX_STAGENAME_LENGTH)

    num_seats = models.IntegerField()
    stage_size = models.CharField(choices=STAGE_SIZE_CHOICES, max_length=1)

    def __str__(self):
        return self.name

    def all_bands(self):
        return Band.objects.filter(concert__stage_name=self)

    def get_absolute_url(self):
        return reverse("stages:detail", args=[self.id])

class Concert(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)
    band_name = models.ForeignKey(Band)
    stage_name = models.ForeignKey(Stage)
    genre_music = models.ForeignKey(Genre)
    #created_time = models.DateTimeField(default=timezone.now, editable=False) #time concert object created
    concert_time = models.DateTimeField(blank=True, null=True) #time concert happening
    concert_description = models.TextField(blank=True)
    light_tech = models.ManyToManyField(User, related_name='light_tech')
    sound_tech = models.ManyToManyField(User, related_name='sound_tech')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('concert:detail', args=[self.id])

    # This model has to be expanded to include which bands are playing, what
    # stage it's happening on, technical requirements, who's performing
    # technical duties.


class Festival(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)
    concerts = models.ManyToManyField(Concert)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('festival:detail', args=[self.id])

    def stages(self):
        return Stage.objects.filter(concert__in=self.concerts.all())

    def concerts_by_stage(self):
        ConcertsByStage = namedtuple('ConcertsByStage', ['stage', 'concerts'])
        concerts = self.concerts.order_by('stage_name')
        grouped = groupby(concerts, lambda c: c.stage_name)
        by_stage = [
            {
                'stage': stage,
                'concerts': sorted(list(concs), key=lambda c: c.concert_time)
            } for stage, concs in grouped
        ]
        return by_stage
