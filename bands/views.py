from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView
from django.core import serializers

from . import models


class StageList(LoginRequiredMixin, ListView):
    model = models.Stage

class StageDetail(DetailView):
    model = models.Stage


class ConcertDetail(LoginRequiredMixin, DetailView):
    model = models.Concert


class ConcertList(LoginRequiredMixin, ListView):
    model = models.Concert

class TechnicianList(LoginRequiredMixin, ListView):
    template_name = "bands/technician_list.html"
    queryset = models.Concert.objects.all()
    def get_template_names(self):
        return self.template_name

    def get_queryset(self):
        user = self.request.user
        users_concerts = models.Concert.objects.all()
        return users_concerts

class GenreList(LoginRequiredMixin, ListView):
    model = models.Genre


class FestivalList(LoginRequiredMixin, ListView):
    model = models.Festival


class FestivalDetail(LoginRequiredMixin, DetailView):
    model = models.Festival


class BandDetail(DetailView):
    model = models.Band

    
class ConcertCreate(CreateView):
    """View for creating concerts. We need to add some JavaScript to compute
    price suggestions, so we can't just use the admin page."""
    model = models.Concert
    fields = '__all__'
    template_name = 'bands/concert_create.html'
    def get_context_data(self):
        context = super().get_context_data()
        context['stage_info'] = serializers.serialize("json", models.Stage.objects.all())
        return context
