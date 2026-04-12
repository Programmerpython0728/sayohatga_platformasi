from __future__ import annotations

from django.core.management.base import BaseCommand

from catalog.models import Accommodation, City, Region, TouristPlace


class Command(BaseCommand):
    help = "Seed demo data (regions/cities/places/accommodations)."

    def handle(self, *args, **options):
        tashkent_region, _ = Region.objects.get_or_create(name="Toshkent viloyati")
        samarkand_region, _ = Region.objects.get_or_create(name="Samarqand viloyati")
        bukhara_region, _ = Region.objects.get_or_create(name="Buxoro viloyati")

        tashkent_city, _ = City.objects.get_or_create(region=tashkent_region, name="Toshkent")
        samarkand_city, _ = City.objects.get_or_create(region=samarkand_region, name="Samarqand")
        bukhara_city, _ = City.objects.get_or_create(region=bukhara_region, name="Buxoro")

        TouristPlace.objects.get_or_create(
            city=samarkand_city,
            name="Registon maydoni",
            defaults={
                "short_description": "Samarqandning eng mashhur tarixiy majmuasi.",
                "description": "Registon maydoni uchta madrasa bilan mashhur: Ulug'bek, Sherdor va Tillaqori.",
            },
        )
        TouristPlace.objects.get_or_create(
            city=bukhara_city,
            name="Ark qal'asi",
            defaults={
                "short_description": "Buxorodagi qadimiy qal'a va saroy majmuasi.",
                "description": "Ark qal'asi Buxoro amirlarining tarixiy qarorgohi bo'lgan.",
            },
        )

        Accommodation.objects.get_or_create(
            city=tashkent_city,
            name="Chorvoq Dacha",
            defaults={
                "type": Accommodation.Type.DACHA,
                "price_per_night": 750000,
                "capacity": 8,
                "short_description": "Tabiat qo'ynida shinam dacha.",
                "description": "Chorvoq atrofida dam olish uchun qulay, oilaviy dacha.",
            },
        )
        Accommodation.objects.get_or_create(
            city=samarkand_city,
            name="Samarqand Hotel",
            defaults={
                "type": Accommodation.Type.HOTEL,
                "price_per_night": 450000,
                "capacity": 3,
                "short_description": "Markazga yaqin, qulay mehmonxona.",
                "description": "Turistlar uchun qulay joylashuv va xizmatlar.",
            },
        )

        self.stdout.write(self.style.SUCCESS("Seeded demo data."))

