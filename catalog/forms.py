from __future__ import annotations

from django import forms

from .models import Accommodation


class PlaceFilterForm(forms.Form):
    q = forms.CharField(required=False)
    region = forms.IntegerField(required=False)
    city = forms.IntegerField(required=False)


class AccommodationFilterForm(forms.Form):
    q = forms.CharField(required=False)
    region = forms.IntegerField(required=False)
    city = forms.IntegerField(required=False)
    type = forms.ChoiceField(required=False, choices=[("", "Any")] + list(Accommodation.Type.choices))
    min_price = forms.IntegerField(required=False, min_value=0)
    max_price = forms.IntegerField(required=False, min_value=0)

