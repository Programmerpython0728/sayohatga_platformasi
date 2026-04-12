from __future__ import annotations

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=120)

    class Meta:
        unique_together = ("region", "name")

    def __str__(self):
        return f"{self.name} ({self.region.name})"


class TouristPlace(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="places")
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=240, blank=True)
    ticket_price = models.PositiveIntegerField(default=0, help_text="Approx ticket price in UZS")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Accommodation(models.Model):
    class Type(models.TextChoices):
        DACHA = "dacha", "Dacha"
        HOTEL = "hotel", "Hotel"
        RESORT = "resort", "Resort"

    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="accommodations")
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=Type.choices)
    price_per_night = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(default=2)
    short_description = models.CharField(max_length=280, blank=True)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=240, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.name


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
