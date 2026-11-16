from __future__ import annotations

from django import forms
from django.utils import timezone

from .models import Booking, PlaceBooking


class BookingCreateForm(forms.ModelForm):
    def __init__(self, *args, min_date=None, max_guests=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_date = min_date or timezone.localdate()
        self.max_guests = max_guests
        min_date_value = self.min_date.isoformat()
        self.fields["date_from"].widget.attrs.update({"min": min_date_value})
        self.fields["date_to"].widget.attrs.update({"min": min_date_value})
        self.fields["guests"].widget.attrs.update({"min": 1})
        if self.max_guests:
            self.fields["guests"].widget.attrs.update({"max": self.max_guests})

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
        guests = data.get("guests")
        if date_from and date_from < self.min_date:
            self.add_error("date_from", "Start date cannot be in the past.")
        if date_from and date_to and date_to < date_from:
            self.add_error("date_to", "End date must be after start date.")
        if self.max_guests and guests and guests > self.max_guests:
            self.add_error("guests", f"Guests cannot exceed accommodation capacity ({self.max_guests}).")
        return data


class PlaceBookingCreateForm(forms.ModelForm):
    def __init__(self, *args, min_date=None, max_visitors=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_date = min_date or timezone.localdate()
        self.max_visitors = max_visitors
        min_date_value = self.min_date.isoformat()
        self.fields["visit_date"].widget.attrs.update({"min": min_date_value})
        self.fields["visitors"].widget.attrs.update({"min": 1})
        if self.max_visitors:
            self.fields["visitors"].widget.attrs.update({"max": self.max_visitors})

    class Meta:
        model = PlaceBooking
        fields = ("visit_date", "visitors", "notes")
        widgets = {
            "visit_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.TextInput(attrs={"placeholder": "Izoh"}),
        }

    def clean(self):
        data = super().clean()
        visit_date = data.get("visit_date")
        visitors = data.get("visitors")
        if visit_date and visit_date < self.min_date:
            self.add_error("visit_date", "Visit date cannot be in the past.")
        if self.max_visitors and visitors and visitors > self.max_visitors:
            self.add_error("visitors", f"Visitors cannot exceed daily limit ({self.max_visitors}).")
        return data
