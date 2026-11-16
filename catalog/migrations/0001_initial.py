from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Region",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                (
                    "region",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cities", to="catalog.region"),
                ),
            ],
            options={"unique_together": {("region", "name")}},
        ),
        migrations.CreateModel(
            name="Accommodation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("type", models.CharField(choices=[("dacha", "Dacha"), ("hotel", "Hotel"), ("resort", "Resort")], max_length=20)),
                ("price_per_night", models.PositiveIntegerField()),
                ("capacity", models.PositiveIntegerField(default=2)),
                ("short_description", models.CharField(blank=True, max_length=280)),
                ("description", models.TextField(blank=True)),
                ("address", models.CharField(blank=True, max_length=240)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "city",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="accommodations", to="catalog.city"),
                ),
            ],
            options={"ordering": ("-created_at",)},
        ),
        migrations.CreateModel(
            name="TouristPlace",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("short_description", models.CharField(blank=True, max_length=280)),
                ("description", models.TextField(blank=True)),
                ("address", models.CharField(blank=True, max_length=240)),
                ("ticket_price", models.PositiveIntegerField(default=0, help_text="Approx ticket price in UZS")),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "city",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="places", to="catalog.city"),
                ),
            ],
            options={"ordering": ("name",)},
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("object_id", models.PositiveBigIntegerField()),
                ("image", models.ImageField(upload_to="gallery/%Y/%m/")),
                ("alt_text", models.CharField(blank=True, max_length=200)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "content_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
                ),
            ],
            options={"ordering": ("sort_order", "id")},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("object_id", models.PositiveBigIntegerField()),
                ("rating", models.PositiveSmallIntegerField(default=5)),
                ("text", models.TextField(blank=True)),
                ("is_approved", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "content_type",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
                ),
                (
                    "user",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to=settings.AUTH_USER_MODEL),
                ),
            ],
            options={"ordering": ("-created_at",)},
        ),
    ]

