from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from catalog.models import Accommodation, TouristPlace

from .forms import BookingCreateForm, PlaceBookingCreateForm
from .models import Booking, PlaceBooking


@login_required
def create_booking(request, accommodation_id: int):
    accommodation = get_object_or_404(Accommodation.objects.select_related("city", "city__region"), pk=accommodation_id)
    min_date = timezone.localdate()

    if request.method == "POST":
        form = BookingCreateForm(
            request.POST,
            min_date=min_date,
            max_guests=accommodation.capacity,
        )
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.accommodation = accommodation
            booking.status = Booking.Status.PENDING
            try:
                booking.full_clean()
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                if booking.overlaps_confirmed():
                    form.add_error(None, "Selected dates are not available (already booked).")
                else:
                    booking.save()
                    messages.success(request, "Booking request created (pending confirmation).")
                    return redirect("accounts:dashboard")
    else:
        form = BookingCreateForm(min_date=min_date, max_guests=accommodation.capacity)

    return render(
        request,
        "bookings/create.html",
        {
            "form": form,
            "accommodation": accommodation,
            "min_date": min_date,
        },
    )


@login_required
def cancel_booking(request, booking_id: int):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == "POST":
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=["status", "updated_at"])
        messages.success(request, "Booking cancelled.")
        return redirect("accounts:dashboard")
    return render(request, "bookings/confirm.html", {"booking": booking})


@login_required
def create_place_booking(request, place_id: int):
    place = get_object_or_404(TouristPlace.objects.select_related("city", "city__region"), pk=place_id)
    if not place.is_bookable:
        messages.error(request, "This tourist place is not available for booking yet.")
        return redirect("places:detail", pk=place.id)

    min_date = timezone.localdate()
    if request.method == "POST":
        form = PlaceBookingCreateForm(
            request.POST,
            min_date=min_date,
            max_visitors=place.max_visitors_per_day,
        )
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.place = place
            booking.status = PlaceBooking.Status.PENDING
            try:
                booking.full_clean()
            except ValidationError as exc:
                form.add_error(None, exc)
            else:
                if booking.exceeds_daily_limit():
                    form.add_error(None, "Selected date limit is full for this place.")
                else:
                    booking.save()
                    messages.success(request, "Tourist place booking request created.")
                    return redirect("accounts:dashboard")
    else:
        form = PlaceBookingCreateForm(min_date=min_date, max_visitors=place.max_visitors_per_day)

    return render(
        request,
        "bookings/place_create.html",
        {
            "form": form,
            "place": place,
            "min_date": min_date,
        },
    )
