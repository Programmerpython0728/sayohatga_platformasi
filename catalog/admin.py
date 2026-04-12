from __future__ import annotations

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import Accommodation, City, Image, Like, Region, Review, TouristPlace


class ImageInline(GenericTabularInline):
    model = Image
    extra = 1
    fields = ("image", "alt_text", "sort_order")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "region")
    list_filter = ("region",)
    search_fields = ("name",)


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "ticket_price")
    list_filter = ("city__region", "city")
    search_fields = ("name", "short_description", "description")
    inlines = [ImageInline]


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "city", "price_per_night", "capacity")
    list_filter = ("type", "city__region", "city")
    search_fields = ("name", "short_description", "description")
    inlines = [ImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("content_type", "object_id", "user", "rating", "is_approved", "created_at")
    list_filter = ("is_approved", "rating", "content_type")
    search_fields = ("text", "user__phone_number")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("user", "content_type", "object_id", "created_at")
    list_filter = ("content_type", "created_at")
    search_fields = ("user__phone_number",)
