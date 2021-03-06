from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout, Submit
from django import forms
from django.contrib.auth.forms import forms
from django.contrib.auth.models import Group, User
from django.utils.timezone import now

from . import models as band_models
from . import groups


class StageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, stage):
        return f'{stage.name} - {stage.get_stage_size_display()} size stage ' \
            f'- {stage.num_seats} seats'


class ConcertChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, concert):
        return f'{concert.name} - {concert.concert_time}'


class FestivalForm(forms.ModelForm):
    class Meta:
        model = band_models.Festival
        exclude = []

    concerts = ConcertChoiceField(
        queryset=band_models.Concert.objects.order_by('-concert_time'),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )


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

    stage = StageChoiceField(
        band_models.Stage.objects,
        help_text="Select a suitable stage",
        required=True
    )

    price = forms.DecimalField(
        help_text="Ticket price you want included in offer. "
        "When selecting a stage, this field will automatically update to the "
        "break-even price assuming the concert sells out.",
        required=True,
        max_digits=15,
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
    acceptable = forms.ChoiceField(
        help_text="Can this offer be sent to the artist?",
        required=True,
        widget=forms.widgets.RadioSelect,
        choices=(
            ('yes', 'Yes, send'),
            ('no', 'No, discard'),

        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        helper = FormHelper()
        self.helper = helper
        helper.add_input(Submit('submit', 'Submit'))


class OfferManagerDetailForm(forms.Form):
    Offer_response = forms.ChoiceField(
        required=True,
        help_text="Approve or disapprove offer",
        choices=((True,'Accept'),(False, 'Decline'))
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
            Field('stage', type='checkbox' if show_stages else 'hidden'),
        )
        self.helper.add_input(Submit('submit', 'Search'))


class ConcertForm(forms.ModelForm):
    class Meta:
        model = band_models.Concert
        exclude = []

    sound_tech = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name=groups.Groups.AUDIO_TECHS.value),
        widget=forms.CheckboxSelectMultiple
    )

    light_tech = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(groups__name=groups.Groups.LIGHT_TECHS.value),
        widget=forms.CheckboxSelectMultiple
    )


class ConcertTechForm(ConcertForm):
    class Meta:
        model = band_models.Concert
        fields = ['light_tech', 'sound_tech']
