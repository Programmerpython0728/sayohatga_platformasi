from django.contrib import admin

from .models import Booking, PlaceBooking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "accommodation", "user", "date_from", "date_to", "guests", "status", "created_at")
    list_filter = ("status", "accommodation__city__region", "accommodation__city", "accommodation")
    search_fields = ("user__phone_number", "accommodation__name")
    autocomplete_fields = ("accommodation", "user")


@admin.register(PlaceBooking)
class PlaceBookingAdmin(admin.ModelAdmin):
    list_display = ("id", "place", "user", "visit_date", "visitors", "status", "created_at")
    list_filter = ("status", "place__city__region", "place__city", "place")
    search_fields = ("user__phone_number", "place__name")
    autocomplete_fields = ("place", "user")
