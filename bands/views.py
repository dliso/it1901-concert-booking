from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.shortcuts import HttpResponse, render
from django.utils import timezone
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView)

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
        results = models.Band.objects.filter(name__contains=query)
        if stages:
            results = results.filter(concert__stage_name__in=stages)
        self.search_results = results
        return self.get(self.request)


class ConcertReport(ListView):
    model = models.Concert
    template_name = 'bands/concert_report.html'
    paginate_by = 15
    queryset = models.Concert.objects.order_by('-concert_time')


class StageEconReport(ListView):
    model = models.Concert
    template_name = 'bands/stage_econ_report.html'
    paginate_by = 15

    def get_object(self):
        return models.Stage.objects.get(pk=self.kwargs['stage_pk'])

    def get_queryset(self):
        stage = self.get_object()
        return self.model.objects.filter(
            stage_name=stage).order_by('-concert_time')

    def compile_stats(self, qs, title):
        num_concerts = len(qs)
        avg_ticket_price = sum([q.ticket_price() for q in qs]) / num_concerts

        return (title, {
            'Total profit': sum([q.profit() for q in qs]),
            'Total tickets sold': sum([q.tickets_sold() for q in qs]),
            'Avg. ticket price': avg_ticket_price,
            'Avg. tickets sold': sum(
                [q.tickets_sold() for q in qs]) / num_concerts,
        })

    def stats_between(self, title, start_date=None, end_date=None):
        qs = self.get_queryset()
        if start_date:
            qs = qs.filter(concert_time__gte=start_date)
        if end_date:
            qs = qs.filter(concert_time__lte=end_date)

        stats = self.compile_stats(qs, title)

        return stats

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['stage'] = self.get_object()

        now = timezone.now()
        thirty_days_ago = now - timezone.timedelta(days=30)
        a_year_ago = now.replace(year=now.year-1)
        context['summary'] = [
            self.stats_between('Last 30 days',
                               start_date=thirty_days_ago,
                               end_date=now),
            self.stats_between('Last year',
                               start_date=a_year_ago,
                               end_date=now),
            self.stats_between('All time'),
        ]

        print(context['summary'])

        return context
