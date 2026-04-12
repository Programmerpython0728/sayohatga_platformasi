from __future__ import annotations

from django import forms
from django.utils import timezone

from .models import Booking


class BookingCreateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("date_from", "date_to", "guests")
        widgets = {
            "date_from": forms.DateInput(attrs={"type": "date"}),
            "date_to": forms.DateInput(attrs={"type": "date"}),
        }

    def clean(self):
        data = super().clean()
        date_from = data.get("date_from")
        date_to = data.get("date_to")
        if date_from and date_from < timezone.localdate():
            self.add_error("date_from", "Start date cannot be in the past.")
        if date_from and date_to and date_to < date_from:
            self.add_error("date_to", "End date must be after start date.")
        return data

