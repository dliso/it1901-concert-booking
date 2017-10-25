from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, render
from django.views.generic import CreateView, DetailView, FormView, ListView

from . import forms, models


class StageList(LoginRequiredMixin, ListView):
    model = models.Stage

class StageDetail(DetailView):
    model = models.Stage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.SearchForm(
            show_stages=False,
            initial={'stage': [self.get_object()]})
        context["form"] = form
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
        self.search_results = models.Band.objects.filter(
            name__contains=query,
            concert__stage_name__in=stages
        )
        return self.get(self.request)
