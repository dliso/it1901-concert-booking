import base64
import colorsys
from collections import namedtuple
from itertools import groupby
from math import sin

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone

MAX_CHARFIELD_LENGTH_GENERAL = 200
MAX_BANDNAME_LENGTH = MAX_CHARFIELD_LENGTH_GENERAL
MAX_STAGENAME_LENGTH = MAX_CHARFIELD_LENGTH_GENERAL


class Genre(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name + " - " + self.description


class Band(models.Model):
    name = models.CharField(max_length=MAX_BANDNAME_LENGTH)
    manager = models.ForeignKey(User, null=True, blank=True)
    genre = models.ForeignKey(Genre)

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


class Stage(models.Model):
    STAGE_SIZE_CHOICES = (('S','Small'),
                          ('M', 'Medium'),
                          ('L', 'Large'))

    name = models.CharField(max_length=MAX_STAGENAME_LENGTH)

    num_seats = models.IntegerField()
    stage_size = models.CharField(choices=STAGE_SIZE_CHOICES, max_length=1)
    stage_costs = models.PositiveIntegerField(default=0)

    def color(self):
        mod = 99
        hue = (sum(map(ord, self.name)) % mod) / mod
        print(hue)
        rgb = colorsys.hsv_to_rgb(hue, 0.5, 0.5)
        r, g, b = map(lambda x: hex(int(255*x))[2:], rgb)
        color = f'#{r}{g}{b}'
        print(color)
        return color

    def __str__(self):
        return self.name

    def all_bands(self):
        return Band.objects.filter(concert__stage_name=self)

    def get_absolute_url(self):
        return reverse("stages:detail", args=[self.id])

    def previous_five_concerts(self):
        return self.concert_set.order_by("-concert_time").filter(concert_time__lte=timezone.now())[:5]

    def upcoming_five_concerts(self):
        return self.concert_set.order_by("concert_time").filter(concert_time__gte=timezone.now())[:5]

    def previous_concerts(self):
        return self.concert_set.order_by("-concert_time").filter(concert_time__lte=timezone.now())

    def upcoming_concerts(self):
        return self.concert_set.order_by("concert_time").filter(concert_time__gte=timezone.now())

    def econ_report_url(self):
        return reverse("stages:econreport", args=[self.id])


class Concert(models.Model):
    name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)
    band_name = models.ForeignKey(Band)
    stage_name = models.ForeignKey(Stage)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    genre_music = models.ForeignKey(Genre)
    #created_time = models.DateTimeField(default=timezone.now, editable=False) #time concert object created
    concert_time = models.DateTimeField(blank=True, null=True) #time concert happening
    concert_description = models.TextField(blank=True)
    light_tech = models.ManyToManyField(User, related_name='light_tech')
    sound_tech = models.ManyToManyField(User, related_name='sound_tech')

    def __str__(self):
        return self.name

    def calendar_title(self):
        return f'{self.stage_name}\n\n{self.name}'

    def json(self):
        return {
            'id': self.pk,
            'title': self.calendar_title(),
            'start': self.concert_time,
            'end': self.concert_time + timezone.timedelta(hours=2),
            'existed': False,
            'event_id': self.pk,
            'rule': None,
            'end_recurring_period': None,
            'calendar': 'default',
            'color': self.stage_name.color(),
            'url': self.get_absolute_url(),
        }

    def get_absolute_url(self):
        return reverse('concert:detail', args=[self.id])

    def edit_tech_url(self):
        return reverse('concert:edit_tech', args=[self.id])

    def tickets_sold(self):
        # TODO Actual implementation
        return 15 * sum(map(len, [self.name, self.band_name.name]))

    def total_expenses(self):
        # TODO Actual implementation
        return 13579 * sum(map(len,
                               [self.stage_name.name, self.band_name.name]))

    def profit(self):
        # TODO Actual implementation
        return self.ticket_price*self.tickets_sold() - self.total_expenses()

    @classmethod
    def upcoming(self):
        return self.objects \
                   .filter(concert_time__gte=timezone.now()) \
                   .order_by('concert_time')

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

    def first_concert(self):
        return self.concerts.order_by('concert_time').first()

    def last_concert(self):
        return self.concerts.order_by('-concert_time').first()


class Offer(models.Model):
    price = models.DecimalField(max_digits=13, decimal_places=2, default=0)
    concert_name = models.CharField(max_length=MAX_CHARFIELD_LENGTH_GENERAL)
    band = models.ForeignKey(Band)
    time = models.DateTimeField(blank=True, null=True)
    accepted_status = models.BooleanField(default=False)
    is_pending_status = models.BooleanField(default=True)
    stage = models.ForeignKey(Stage)
    genre = models.ForeignKey(Genre)
    concert_description = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('offer:offerDetail', args=[self.id])

    @classmethod
    def pending(self):
        return self.objects.filter(is_pending_status=True)

    @classmethod
    def accepted(self):
        return self.objects.filter(accepted_status=True)

    @classmethod
    def rejected(self):
        return self.objects.filter(is_pending_status=False, accepted_status=False)

    def status(self):
        if self.accepted_status:
            return 'Accepted'
        elif self.is_pending_status:
            return 'Pending'
        else:
            return 'Rejected'
