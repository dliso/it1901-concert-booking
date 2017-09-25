from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from bands import models as band_models


class SignUpForm(UserCreationForm):
    groups = forms.ModelMultipleChoiceField(
        Group.objects, help_text="Select the groups you would like to be made"
        " a member of.", required=False)
    bands = forms.ModelMultipleChoiceField(
        band_models.Band.objects, help_text="Select the bands you would like"
        " to be made a manager for.",
        required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = FormHelper()
        self.helper = helper
        helper.add_input(Submit('submit', 'Submit'))
