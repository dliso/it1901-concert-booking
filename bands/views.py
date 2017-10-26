from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from . import models, forms
from django.contrib.auth.models import User, Group


class StageList(LoginRequiredMixin, ListView):
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



class OfferView(FormView):
    form_class = forms.OfferForm
    template_name = 'bands/offer.html'

    def get_success_url(self):
        req = self.request
        return req.GET.get('next', '/')

    def form_valid(self, form):
        data = form.cleaned_data
        o = models.Offer()
        o.band = data['band']
        o.price = data['price']
        o.time = data['time']
        o.save()

        return super().form_valid(form)

class OfferList(ListView):
    model = models.Offer
    template_name = 'bands/offer_list.html'

class OfferDetail(DetailView):
    model = models.Offer


class OfferDetail(FormView):
    form_class = forms.OfferDetailForm
    template_name = 'bands/offer_detail.html'

    def get_success_url(self):
        req = self.request
        return req.GET.get('next', '/')

    def form_valid(self, form):
        data = form.cleaned_data
        if data['acceptable'] == True:
            n = 1
        else:
            n = 2

        return super().form_valid(form)