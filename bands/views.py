from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.mixins import UserPassesTestMixin

from . import models, forms
from django.contrib.auth.models import User, Group


class StageList(LoginRequiredMixin, ListView):
    model = models.Stage


class ConcertDetail(LoginRequiredMixin, DetailView, FormView):
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



class OfferView(UserPassesTestMixin, FormView):
    form_class = forms.OfferForm
    template_name = 'bands/offer.html'


    def test_func(self):
        return self.request.user.groups.filter(name="booking_responsibles").exists()


    def get_success_url(self):
        req = self.request
        return req.GET.get('next', '/')

    def form_valid(self, form):
        data = form.cleaned_data
        o = models.Offer()
        o.band = data['band']
        o.concert_description = data['concert_description']
        o.concert_name = data['concert_name']
        o.stage = data['stage']
        o.genre = o.band.genre
        o.price = data['price']
        o.time = data['time']
        o.save()

        return super().form_valid(form)

class OfferList(UserPassesTestMixin, ListView):
    model = models.Offer
    template_name = 'bands/offer_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name="booking_chiefs").exists()


class OfferDetail(UserPassesTestMixin, FormView, DetailView):
    model = models.Offer
    form_class = forms.OfferDetailForm
    template_name = 'bands/offer_detail.html'


    def test_func(self):
        return self.request.user.groups.filter(name="booking_chiefs").exists()

    def get_success_url(self):
        req = self.request
        return req.GET.get('next', '/offer')

    def form_valid(self, form):
        data = form.cleaned_data
        if data['acceptable'] == True:
            offers = models.Offer.objects.all()
            for o in offers:
                if str(o.id) == self.kwargs['pk']:
                    o.is_pending_status = False
                    o.save()
        return super().form_valid(form)

class OfferManagerList(UserPassesTestMixin, ListView):
    model = models.Offer
    template_name = 'bands/offerManager_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name="managers").exists()

class OfferManagerDetail(UserPassesTestMixin, FormView, DetailView):
    model = models.Offer
    form_class = forms.OfferManagerDetailForm
    template_name = 'bands/offerManager_detail.html'

    def test_func(self):
        return self.request.user.groups.filter(name="managers").exists()

    def get_success_url(self):
        req = self.request
        return req.GET.get('next', '/offer/manager')

    def form_valid(self, form):
        data = form.cleaned_data
        if data['acceptable'] == True:
            offers = models.Offer.objects.all()
            for o in offers:
                if str(o.id) == self.kwargs['pk']:
                    o.accepted_status = True

                    c = models.Concert()
                    c.name = o.concert_name
                    c.band_name = o.band
                    c.stage_name = o.stage
                    c.genre_music = o.band.genre
                    c.concert_time = o.time
                    c.concert_description = o.concert_description

                    o.save()
                    c.save()
        return super().form_valid(form)
