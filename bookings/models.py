from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    accommodation = models.ForeignKey("catalog.Accommodation", on_delete=models.CASCADE, related_name="bookings")

    date_from = models.DateField()
    date_to = models.DateField()
    guests = models.PositiveIntegerField(default=1)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["accommodation", "date_from", "date_to"]),
        ]

    def __str__(self):
        return f"{self.accommodation.name} ({self.date_from} - {self.date_to})"

    def clean(self):
        if self.date_from and self.date_to and self.date_to < self.date_from:
            raise ValidationError({"date_to": "End date must be after start date."})
        if self.guests <= 0:
            raise ValidationError({"guests": "Guests must be positive."})

    def overlaps_confirmed(self) -> bool:
        qs = Booking.objects.filter(
            accommodation=self.accommodation,
            status=Booking.Status.CONFIRMED,
        )
        if self.pk:
            qs = qs.exclude(pk=self.pk)
        # Overlap: [a,b] overlaps [c,d] if a <= d and c <= b
        return qs.filter(date_from__lte=self.date_to, date_to__gte=self.date_from).exists()
