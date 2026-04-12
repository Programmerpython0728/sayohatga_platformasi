from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "accommodation", "user", "date_from", "date_to", "guests", "status", "created_at")
    list_filter = ("status", "accommodation__city__region", "accommodation__city", "accommodation")
    search_fields = ("user__phone_number", "accommodation__name")
    autocomplete_fields = ("accommodation", "user")

