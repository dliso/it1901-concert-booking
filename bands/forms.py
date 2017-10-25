from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, BaseInput, Div, Field, Layout, Submit
from django import forms

from . import models


class SearchForm(forms.Form):
    query = forms.fields.CharField(required=False,
                                   label="Band name")
    stage = forms.ModelMultipleChoiceField(
        models.Stage.objects,
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