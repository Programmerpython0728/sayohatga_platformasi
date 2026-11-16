from __future__ import annotations

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from catalog.models import Accommodation, Image, Like, Review, TouristPlace


class Command(BaseCommand):
    help = "Delete places/accommodations that have no images (and clean related likes/reviews)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--places",
            action="store_true",
            help="Cleanup TouristPlace records without images.",
        )
        parser.add_argument(
            "--accommodations",
            action="store_true",
            help="Cleanup Accommodation records without images.",
        )
        parser.add_argument("--dry-run", action="store_true", help="Print counts but do not delete anything.")

    def handle(self, *args, **options):
        do_places = bool(options["places"])
        do_acc = bool(options["accommodations"])
        dry = bool(options["dry_run"])

        if not do_places and not do_acc:
            do_places = True
            do_acc = True

        total_deleted = 0

        if do_places:
            total_deleted += self._cleanup_model(TouristPlace, dry=dry)
        if do_acc:
            total_deleted += self._cleanup_model(Accommodation, dry=dry)

        if dry:
            self.stdout.write(self.style.WARNING("Dry run complete. No data was deleted."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Cleanup complete. Deleted {total_deleted} objects."))

    def _cleanup_model(self, model_cls, dry: bool) -> int:
        ct = ContentType.objects.get_for_model(model_cls)
        image_object_ids = (
            Image.objects.filter(content_type=ct)
            .values_list("object_id", flat=True)
            .distinct()
        )
        qs = model_cls.objects.exclude(id__in=image_object_ids)
        count = qs.count()

        self.stdout.write(f"{model_cls.__name__}: {count} objects without images.")
        if count == 0:
            return 0
        if dry:
            return 0

        object_ids = list(qs.values_list("id", flat=True))
        # Clean generic relations (no cascade).
        try:
            Like.objects.filter(content_type=ct, object_id__in=object_ids).delete()
        except OperationalError:
            pass
        try:
            Review.objects.filter(content_type=ct, object_id__in=object_ids).delete()
        except OperationalError:
            pass

        deleted, _ = qs.delete()
        return deleted
