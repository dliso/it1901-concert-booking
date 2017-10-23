from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from rules.contrib.views import PermissionRequiredMixin

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

class BandList(ListView):
    model = models.Band

class FestivalPRDetail(PermissionRequiredMixin, DetailView):
    model = models.Festival
    template_name = "bands/festival_pr_detail.html"

    permission_required = 'bands.concert.view_pr_details'
