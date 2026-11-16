from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("catalog", "0001_initial"),
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Like",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("object_id", models.PositiveBigIntegerField()),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("content_type", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "unique_together": {("user", "content_type", "object_id")},
            },
        ),
        migrations.AddIndex(
            model_name="like",
            index=models.Index(fields=["content_type", "object_id"], name="catalog_lik_content_1a1be0_idx"),
        ),
        migrations.AddIndex(
            model_name="like",
            index=models.Index(fields=["user", "created_at"], name="catalog_lik_user_id_1a9f4c_idx"),
        ),
    ]

