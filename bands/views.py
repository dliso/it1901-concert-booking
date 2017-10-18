from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView

from . import models


class StageList(ListView):
    model = models.Stage


class ConcertDetail(DetailView):
    model = models.Concert


class ConcertList(ListView):
    model = models.Concert

class TechnicianList(ListView):
    template_name = "bands/technician_list.html"
    queryset = models.Concert.objects.all()
    def get_template_names(self):
        return self.template_name

    def get_queryset(self):
        user = self.request.user
        users_concerts = models.Concert.objects.all()
        return users_concerts

class GenreList(ListView):
    model = models.Genre


class FestivalList(ListView):
    model = models.Festival


class FestivalDetail(DetailView):
    model = models.Festival


class ConcertCreate(CreateView):
    """View for creating concerts. We need to add some JavaScript to compute
    price suggestions, so we can't just use the admin page."""
    model = models.Concert
    fields = '__all__'
    template_name = 'bands/concert_create.html'
