from django.shortcuts import render
from django.views.generic import DetailView, ListView

from . import models


class StageList(ListView):
    model = models.Stage

class ConcertList(ListView):
    model = models.Concert


class GenreList(ListView):
    model = models.Genre


class FestivalList(ListView):
    model = models.Festival


class FestivalDetail(DetailView):
    model = models.Festival
