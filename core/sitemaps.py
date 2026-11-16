from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from catalog.models import Accommodation, TouristPlace


class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return ["home", "places:list", "accommodations:list"]

    def location(self, item):
        return reverse(item)


class PlaceSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"
    protocol = "https"
    limit = 2000

    def items(self):
        return TouristPlace.objects.select_related("city").order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at


class AccommodationSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"
    protocol = "https"
    limit = 2000

    def items(self):
        return Accommodation.objects.select_related("city").order_by("-created_at")

    def lastmod(self, obj):
        return obj.created_at


SITEMAPS = {
    "static": StaticViewSitemap,
    "places": PlaceSitemap,
    "accommodations": AccommodationSitemap,
}
