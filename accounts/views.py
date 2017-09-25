from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import FormView, ListView

from . import forms


class Dashboard(ListView):
    model = User


class SignUpView(FormView):
    form_class = forms.SignUpForm
    template_name = 'registration/signup.html'
    success_url = '.'

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)
