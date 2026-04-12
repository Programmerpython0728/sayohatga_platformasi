from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect, render
from django.urls import reverse

from catalog.models import Accommodation, Image, Region, TouristPlace


def home(request):
    regions = Region.objects.all().order_by("name")[:8]
    # Prefer showing items that have images (to avoid empty cards on the homepage).
    raw_places = list(
        TouristPlace.objects.select_related("city", "city__region").order_by("-created_at")[:30]
    )
    raw_accommodations = list(
        Accommodation.objects.select_related("city", "city__region").order_by("-created_at")[:30]
    )

    def first_image_map(model_cls, ids):
        if not ids:
            return {}
        ct = ContentType.objects.get_for_model(model_cls)
        imgs = Image.objects.filter(content_type=ct, object_id__in=ids).order_by("object_id", "sort_order", "id")
        mapping = {}
        for img in imgs:
            if img.object_id not in mapping:
                mapping[img.object_id] = img
        return mapping

    place_images_all = first_image_map(TouristPlace, [p.id for p in raw_places])
    acc_images_all = first_image_map(Accommodation, [a.id for a in raw_accommodations])

    places = [p for p in raw_places if p.id in place_images_all][:9]
    accommodations = [a for a in raw_accommodations if a.id in acc_images_all][:9]

    if not places:
        places = raw_places[:9]
    if not accommodations:
        accommodations = raw_accommodations[:9]

    place_images = first_image_map(TouristPlace, [p.id for p in places])
    acc_images = first_image_map(Accommodation, [a.id for a in accommodations])

    return render(
        request,
        "core/home.html",
        {
            "regions": regions,
            "places": places,
            "accommodations": accommodations,
            "place_images": place_images,
            "acc_images": acc_images,
        },
    )


def set_site_language(request, code: str):
    from .i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

    if code not in SUPPORTED_LANGUAGES:
        code = DEFAULT_LANGUAGE
    request.session["site_language"] = code
    next_url = request.GET.get("next") or request.META.get("HTTP_REFERER") or reverse("core:home")
    response = redirect(next_url)
    response.set_cookie("site_language", code, max_age=60 * 60 * 24 * 365)
    return response


def language_root_redirect(request, code: str):
    return set_site_language(request, code)
