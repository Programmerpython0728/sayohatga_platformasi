from __future__ import annotations

from django.core.management.base import BaseCommand

from catalog.models import Accommodation, City, Region, TouristPlace


class Command(BaseCommand):
    help = "Remove demo data created by seed_demo (by known names)."

    def handle(self, *args, **options):
        TouristPlace.objects.filter(name__in=["Registon maydoni", "Ark qal'asi"]).delete()
        Accommodation.objects.filter(name__in=["Chorvoq Dacha", "Samarqand Hotel"]).delete()
        City.objects.filter(name__in=["Toshkent", "Samarqand", "Buxoro"]).delete()
        Region.objects.filter(name__in=["Toshkent viloyati", "Samarqand viloyati", "Buxoro viloyati"]).delete()
        self.stdout.write(self.style.SUCCESS("Demo data removed (if it existed)."))

