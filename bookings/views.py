from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render

from catalog.models import Accommodation

from .forms import BookingCreateForm
from .models import Booking


@login_required
def create_booking(request, accommodation_id: int):
    accommodation = get_object_or_404(Accommodation.objects.select_related("city", "city__region"), pk=accommodation_id)

    if request.method == "POST":
        form = BookingCreateForm(request.POST)
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
        form = BookingCreateForm()

    return render(
        request,
        "bookings/booking_create.html",
        {"form": form, "accommodation": accommodation},
    )


@login_required
def cancel_booking(request, booking_id: int):
    booking = get_object_or_404(Booking, pk=booking_id, user=request.user)
    if request.method == "POST":
        booking.status = Booking.Status.CANCELLED
        booking.save(update_fields=["status", "updated_at"])
        messages.success(request, "Booking cancelled.")
        return redirect("accounts:dashboard")
    return render(request, "bookings/booking_cancel.html", {"booking": booking})
