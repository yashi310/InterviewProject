from django import forms
from django.forms import ModelForm
from . models import *


class CreateForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['start','end', 'members']
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    members = forms.ModelMultipleChoiceField(
        queryset=Member.objects.all(),
        widget=forms.CheckboxSelectMultiple

    )