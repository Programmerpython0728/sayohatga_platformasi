from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TelegramOtp",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone_number", models.CharField(db_index=True, max_length=20)),
                ("code_hash", models.CharField(max_length=256)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
                ("attempts_used", models.PositiveIntegerField(default=0)),
                ("max_attempts", models.PositiveIntegerField(default=5)),
                ("is_used", models.BooleanField(default=False)),
            ],
        ),
        migrations.AddIndex(
            model_name="telegramotp",
            index=models.Index(fields=["phone_number", "expires_at"], name="integrations_phone_expires_idx"),
        ),
    ]

