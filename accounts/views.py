from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from django.views.generic import FormView, ListView

from bands import models as band_models

from . import forms


class Dashboard(LoginRequiredMixin, ListView):
    model = User
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['band_list'] = band_models.Band.objects.all()
        context['stage_list'] = band_models.Stage.objects.all()
        context['festival_list'] = band_models.Festival.objects.all()
        context['group_list'] = Group.objects.all()
        context['concert_list'] = band_models.Concert.objects.all()
        context['upcoming_concerts'] = band_models.Concert.upcoming()[:5]
        return context


class SignUpView(FormView):
    form_class = forms.SignUpForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        req = self.request
        return req.GET.get('next', '/')

    def form_valid(self, form):
        data = form.cleaned_data
        # Create user
        u = User.objects.create_user(data['username'], password=data['password1'])
        u.save()
        # Add user to groups
        for group in data['groups']:
            u.groups.add(group)

        # TODO
        # Create any requested new bands

        # Add user as band manager of selected bands
        for band in data['bands']:
            band.manager = u
            band.save()

        # TODO
        # Don't just hand over bands because people asked for it.

        # Log user in
        login(self.request, u)

        return super().form_valid(form)
