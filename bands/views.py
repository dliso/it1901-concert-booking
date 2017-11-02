from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core import serializers
from django.db.models import Count, Min
from django.utils import timezone
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView)
from rules.contrib.views import PermissionRequiredMixin

from . import forms, models


class StageList(LoginRequiredMixin, ListView):
    model = models.Stage
    paginate_by = 12
    queryset = models.Stage.objects \
                     .annotate(num_concerts=Count('concert')) \
                     .order_by('-num_concerts')

class StageDetail(DetailView):
    model = models.Stage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = forms.SearchForm(
            show_stages=False,
            initial={'stage': [self.get_object()]})
        context["form"] = form
        return context


class ConcertDetail(LoginRequiredMixin, DetailView, FormView):
    model = models.Concert




class ConcertList(LoginRequiredMixin, ListView):
    model = models.Concert
    paginate_by = 12
    queryset = models.Concert.objects.order_by('-concert_time')

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
    paginate_by = 6
    queryset = models.Festival \
                     .objects \
                     .annotate(start_time=Min('concerts__concert_time')) \
                     .order_by('-start_time')


class FestivalDetail(LoginRequiredMixin, DetailView):
    model = models.Festival


class BookingDashboard(TemplateView):
    template_name = 'bands/booking_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pending_offers'] = models.Offer.pending()[:5]
        context['accepted_offers'] = models.Offer.accepted()[:5]
        context['rejected_offers'] = models.Offer.rejected()[:5]
        return context


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


class BandDetail(DetailView):
    model = models.Band


class BandList(ListView):
    model = models.Band
    paginate_by = 24


class ConcertCreate(CreateView):
    """View for creating concerts. We need to add some JavaScript to compute
    price suggestions, so we can't just use the admin page."""
    model = models.Concert
    template_name = 'bands/concert_create.html'
    form_class = forms.ConcertForm

    def get_context_data(self):
        context = super().get_context_data()
        context['stage_info'] = serializers.serialize("json", models.Stage.objects.all())
        return context


class ConcertEdit(PermissionRequiredMixin, UpdateView):
    """View for creating concerts. We need to add some JavaScript to compute
    price suggestions, so we can't just use the admin page."""
    model = models.Concert
    template_name = 'bands/concert_create.html'
    form_class = forms.ConcertForm

    permission_required = 'concert.edit'


class ConcertEditTech(PermissionRequiredMixin, UpdateView):
    """View for creating concerts. We need to add some JavaScript to compute
    price suggestions, so we can't just use the admin page."""
    model = models.Concert
    template_name = 'bands/concert_create.html'
    form_class = forms.ConcertTechForm

    permission_required = 'concert.edit_tech_staff'

    
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
            results = results.filter(concert__stage_name=stages).distinct()
        self.search_results = results
        return self.get(self.request)


class ConcertReport(ListView):
    model = models.Concert
    template_name = 'bands/concert_report.html'
    paginate_by = 15
    queryset = models.Concert.objects.order_by('-concert_time')


class StageEconReport(PermissionRequiredMixin, ListView):
    model = models.Concert
    template_name = 'bands/stage_econ_report.html'
    paginate_by = 15
    permission_required = 'stage.view_econ_report'

    def get_object(self):
        return models.Stage.objects.get(pk=self.kwargs['stage_pk'])

    def get_queryset(self):
        stage = self.get_object()
        return self.model.objects.filter(
            stage_name=stage).order_by('-concert_time')

    def compile_stats(self, qs, title):
        num_concerts = len(qs)
        if num_concerts == 0:
            return (title, {
                'No tickets sold': '',
            })
        avg_ticket_price = sum([q.ticket_price for q in qs]) / num_concerts

        top_concert = sorted(qs, key=lambda q: -q.profit())[0]
        avg_tickets_sold = sum([q.tickets_sold() for q in qs]) / num_concerts

        return (title, {
            'Total profit': sum([q.profit() for q in qs]),
            'Total tickets sold': sum([q.tickets_sold() for q in qs]),
            'Avg. ticket price': f'{avg_ticket_price:.2f}',
            'Avg. tickets sold': f'{avg_tickets_sold:.2f}',
            'Top band': f'{top_concert.band_name}\n{top_concert.profit()}',
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
