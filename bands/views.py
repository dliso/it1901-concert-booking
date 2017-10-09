from django.shortcuts import render
from django.views.generic import ListView

from . import models

class StageList(ListView):
    model = models.Stage

class ConcertList(ListView):
    model = models.Concert

class TeknikerList(ListView):
    template_name = "bands/tekniker_list.html"
    queryset = models.Concert.objects.all()
    def get_template_names(self):
        return self.template_name

    def get_queryset(self):
       user = self.request.user
       users_concerts = models.Concert.objects.all()
       return users_concerts

class GenreList(ListView):
    model = models.Genre



