from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms

from . import models as band_models


class OfferForm(forms.Form):
    concert_name = forms.CharField(
        help_text="What you would like the name of your concert to be",
        required=True,
    )

    concert_description = forms.CharField(
        widget=forms.Textarea,
        help_text="Give a description off the concert you wish to create",
        required=True,
    )

    price = forms.DecimalField(help_text="Give price you want included in offer",
                               required=True,
                               max_digits=15,
    )

    stage = forms.ModelChoiceField(
        band_models.Stage.objects,
        help_text="Select a suitable stage",
        required=True
    )

    band = forms.ModelChoiceField(
        band_models.Band.objects, help_text="Select the band you want included in your offer",
        required=True)

    time = forms.DateTimeField(
        required=True,
        help_text="Select the date you want the offers concert to be set",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = FormHelper()
        self.helper = helper
        helper.add_input(Submit('submit', 'Submit'))


class OfferDetailForm(forms.Form):
    acceptable = forms.BooleanField(
        required=True,
        help_text="Approve or disapprove offer"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = FormHelper()
        self.helper = helper
        helper.add_input(Submit('submit', 'Submit'))


class OfferManagerDetailForm(forms.Form):
    acceptable = forms.BooleanField(
        required=True,
        help_text="Approve or disapprove offer"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = FormHelper()
        self.helper = helper
        helper.add_input(Submit('submit', 'Submit'))


class SearchForm(forms.Form):
    query = forms.fields.CharField(required=False,
                                   label="Band name")
    stage = forms.ModelMultipleChoiceField(
        band_models.Stage.objects,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Restrict results to bands that have performed on all the selected stages."
    )

    def __init__(self, *args, show_stages=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'query',
            Div(Field('stage', type='' if show_stages else 'hidden', css_class="highlight"), css_class="horizontal-checkboxes")
        )
        self.helper.add_input(Submit('submit', 'Search'))
