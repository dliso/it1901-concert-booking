from django.shortcuts import render
from django.views.generic import ListView

from . import models

class StageList(ListView):
    model = models.Stage

class ConcertList(ListView):
    model = models.Concert


class GenreList(ListView):
    model = models.Genre


