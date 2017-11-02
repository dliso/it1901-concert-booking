from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, render
from django.views.generic import CreateView, DetailView, FormView, ListView

from . import forms, models


class StageList(LoginRequiredMixin, ListView):
    model = models.Stage

class StageDetail(DetailView):
    model = models.Stage
    show_upcoming = 0
    show_previous = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.SearchForm(
            show_stages=False,
            initial={'stage': [self.get_object()]})
        context["form"] = form
        context["upcoming_concerts"] = \
            self.get_object() \
                .upcoming_concerts()[:(None if self.show_upcoming == 'all'
                                       else self.show_upcoming)]
        context["previous_concerts"] = \
            self.get_object() \
                .previous_concerts()[:(None if self.show_previous == 'all'
                                       else self.show_previous)]
        return context


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

    
class ConcertCreate(CreateView):
    """View for creating concerts. We need to add some JavaScript to compute
    price suggestions, so we can't just use the admin page."""
    model = models.Concert
    fields = '__all__'
    template_name = 'bands/concert_create.html'


class BandSearch(FormView):
    form_class = forms.SearchForm
    success_url = "."
    template_name = "bands/band_search.html"
    search_results = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_results'] = self.search_results
        return context

    def form_valid(self, form):
        print(form.data)
        stages = form.data.get('stage', [])
        query = form.data.get('query', '')
        results = models.Band.objects.filter(name__contains=query)
        if stages:
            results = results.filter(concert__stage_name__in=stages)
        self.search_results = results
        return self.get(self.request)
