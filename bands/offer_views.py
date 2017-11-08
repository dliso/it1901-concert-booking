from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView)
from rules.contrib.views import PermissionRequiredMixin

from . import forms, models


class Create(PermissionRequiredMixin, FormView):
    form_class = forms.OfferForm
    template_name = 'bands/offer_create.html'
    permission_required = "offer.view"

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

class OfferList(PermissionRequiredMixin, ListView):
    model = models.Offer
    template_name = 'bands/offer_list.html'
    permission_required = "offerlist.view"



class OfferDetail(PermissionRequiredMixin, FormView, DetailView):
    model = models.Offer
    form_class = forms.OfferDetailForm
    template_name = 'bands/offer_detail.html'
    permission_required = "offerlist.view"

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

class OfferManagerList(PermissionRequiredMixin, ListView):
    model = models.Offer
    template_name = 'bands/offerManager_list.html'
    permission_required = "offermanager.view"


class OfferManagerDetail(PermissionRequiredMixin, FormView, DetailView):
    model = models.Offer
    form_class = forms.OfferManagerDetailForm
    template_name = 'bands/offerManager_detail.html'
    permission_required = "offermanager.view"

    def get_success_url(self):
        req = self.request
        return req.GET.get('next', '/offer/manager')

    def form_valid(self, form):
        data = form.cleaned_data
        offers = models.Offer.objects.all()
        for o in offers:
            if str(o.id) == self.kwargs['pk']:
                if data['Offer_response'] == True:
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
                else:
                    o.rejected_status = True
                    o.save()
        return super().form_valid(form)
