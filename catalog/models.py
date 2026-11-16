from __future__ import annotations

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils import translation
from django.utils.functional import cached_property


def current_language() -> str:
    code = (translation.get_language() or "uz").split("-")[0].lower()
    return code if code in {"uz", "ru", "en"} else "uz"


class TranslatableFieldsMixin(models.Model):
    class Meta:
        abstract = True

    def translated_value(self, field_name: str) -> str:
        lang = current_language()
        if lang == "ru":
            translated = getattr(self, f"{field_name}_ru", "") or ""
            return translated.strip() or getattr(self, field_name, "")
        if lang == "en":
            translated = getattr(self, f"{field_name}_en", "") or ""
            return translated.strip() or getattr(self, field_name, "")
        return getattr(self, field_name, "")


class Region(TranslatableFieldsMixin, models.Model):
    name = models.CharField(max_length=120, unique=True)
    name_ru = models.CharField(max_length=120, blank=True)
    name_en = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return self.translated_name

    @property
    def translated_name(self) -> str:
        return self.translated_value("name")


class City(TranslatableFieldsMixin, models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=120)
    name_ru = models.CharField(max_length=120, blank=True)
    name_en = models.CharField(max_length=120, blank=True)

    class Meta:
        unique_together = ("region", "name")

    def __str__(self):
        return f"{self.translated_name} ({self.region.translated_name})"

    @property
    def translated_name(self) -> str:
        return self.translated_value("name")


class TouristPlace(TranslatableFieldsMixin, models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200, blank=True)
    name_en = models.CharField(max_length=200, blank=True)
    short_description = models.CharField(max_length=280, blank=True)
    short_description_ru = models.CharField(max_length=280, blank=True)
    short_description_en = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    address = models.CharField(max_length=240, blank=True)
    address_ru = models.CharField(max_length=240, blank=True)
    address_en = models.CharField(max_length=240, blank=True)
    ticket_price = models.PositiveIntegerField(default=0, help_text="Approx ticket price in UZS")
    is_bookable = models.BooleanField(default=False)
    max_visitors_per_day = models.PositiveIntegerField(default=50)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("name",)
        indexes = [
            models.Index(fields=["name"], name="place_name_idx"),
            models.Index(fields=["city", "name"], name="place_city_name_idx"),
            models.Index(fields=["-created_at"], name="place_created_idx"),
        ]

    def __str__(self):
        return self.translated_name

    def get_absolute_url(self) -> str:
        from django.urls import reverse
        return reverse("places:detail", args=[self.pk])

    @property
    def slug(self) -> str:
        return str(self.pk)

    @property
    def region(self):
        return self.city.region

    @cached_property
    def cover_image(self):
        # View'lar image_map orqali oldindan to'ldirishi mumkin (N+1 oldini olish uchun).
        images = self.images
        return images[0] if images else None

    @cached_property
    def images(self):
        ct = ContentType.objects.get_for_model(TouristPlace)
        return list(
            Image.objects.filter(content_type=ct, object_id=self.pk).order_by("sort_order", "id")
        )

    @cached_property
    def reviews(self):
        ct = ContentType.objects.get_for_model(TouristPlace)
        return list(
            Review.objects.filter(content_type=ct, object_id=self.pk, is_approved=True)
            .select_related("user")
            .order_by("-created_at")
        )

    @property
    def map_query(self) -> str:
        parts = [self.translated_address, self.city.translated_name, self.city.region.translated_name, "Uzbekistan"]
        return ", ".join(part for part in parts if part)

    @property
    def translated_name(self) -> str:
        return self.translated_value("name")

    @property
    def translated_short_description(self) -> str:
        return self.translated_value("short_description")

    @property
    def translated_description(self) -> str:
        return self.translated_value("description")

    @property
    def translated_address(self) -> str:
        return self.translated_value("address")


class Accommodation(TranslatableFieldsMixin, models.Model):
    class Type(models.TextChoices):
        DACHA = "dacha", "Dacha"
        HOTEL = "hotel", "Hotel"
        RESORT = "resort", "Resort"

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="accommodations")
    name = models.CharField(max_length=200)
    name_ru = models.CharField(max_length=200, blank=True)
    name_en = models.CharField(max_length=200, blank=True)
    type = models.CharField(max_length=20, choices=Type.choices)
    price_per_night = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=2)
    short_description = models.CharField(max_length=280, blank=True)
    short_description_ru = models.CharField(max_length=280, blank=True)
    short_description_en = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)
    description_ru = models.TextField(blank=True)
    description_en = models.TextField(blank=True)
    address = models.CharField(max_length=240, blank=True)
    address_ru = models.CharField(max_length=240, blank=True)
    address_en = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["-created_at"], name="acc_created_idx"),
            models.Index(fields=["type"], name="acc_type_idx"),
            models.Index(fields=["price_per_night"], name="acc_price_idx"),
            models.Index(fields=["city", "-created_at"], name="acc_city_created_idx"),
        ]

    def __str__(self):
        return self.translated_name

    def get_absolute_url(self) -> str:
        from django.urls import reverse
        return reverse("accommodations:detail", args=[self.pk])

    @property
    def slug(self) -> str:
        return str(self.pk)

    @property
    def region(self):
        return self.city.region

    @cached_property
    def cover_image(self):
        images = self.images
        return images[0] if images else None

    @cached_property
    def images(self):
        ct = ContentType.objects.get_for_model(Accommodation)
        return list(
            Image.objects.filter(content_type=ct, object_id=self.pk).order_by("sort_order", "id")
        )

    @cached_property
    def reviews(self):
        ct = ContentType.objects.get_for_model(Accommodation)
        return list(
            Review.objects.filter(content_type=ct, object_id=self.pk, is_approved=True)
            .select_related("user")
            .order_by("-created_at")
        )

    @property
    def translated_name(self) -> str:
        return self.translated_value("name")

    @property
    def translated_short_description(self) -> str:
        return self.translated_value("short_description")

    @property
    def translated_description(self) -> str:
        return self.translated_value("description")

    @property
    def translated_address(self) -> str:
        return self.translated_value("address")


class Image(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    image = models.ImageField(upload_to="gallery/%Y/%m/")
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("sort_order", "id")

    def __str__(self):
        return self.alt_text or f"Image {self.id}"


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    rating = models.PositiveSmallIntegerField(default=5)
    text = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.rating}/5"

    @property
    def comment(self) -> str:
        return self.text


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "content_type", "object_id")
        indexes = [
            models.Index(fields=["content_type", "object_id"], name="catalog_lik_content_1a1be0_idx"),
            models.Index(fields=["user", "created_at"], name="catalog_lik_user_id_1a9f4c_idx"),
        ]

    def __str__(self):
        return f"{self.user_id} likes {self.content_type_id}:{self.object_id}"


@receiver([post_save, post_delete], sender=Region)
def _clear_nav_regions_cache(sender, **kwargs):
    # core.context_processors.get_nav_regions bilan bir xil kalit
    cache.delete("nav_regions_v1")
