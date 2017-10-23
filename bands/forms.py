from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, BaseInput, Div, Field, Layout, Submit
from django import forms

from . import models


class SearchForm(forms.Form):
    query = forms.fields.CharField(required=False)
    stage = forms.ModelMultipleChoiceField(
        models.Stage.objects,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'query',
            'stage'
        )
        self.helper.add_input(Submit('submit', 'Submit'))
