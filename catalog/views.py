from __future__ import annotations

from urllib.parse import quote_plus

from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db.utils import OperationalError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import AccommodationFilterForm, PlaceFilterForm
from .models import Accommodation, City, Image, Like, Region, Review, TouristPlace


def _basket_key(kind: str, object_id: int) -> str:
    return f"{kind}:{object_id}"


def _basket_state(model_cls, object_ids: list[int], request) -> set[int]:
    kind = "place" if model_cls is TouristPlace else "accommodation"
    basket = set(request.session.get("basket_items", []))
    return {object_id for object_id in object_ids if _basket_key(kind, object_id) in basket}


def _first_image_map(model_cls, object_ids: list[int]) -> dict[int, Image]:
    if not object_ids:
        return {}
    ct = ContentType.objects.get_for_model(model_cls)
    images = (
        Image.objects.filter(content_type=ct, object_id__in=object_ids)
        .order_by("object_id", "sort_order", "id")
        .only("id", "image", "alt_text", "object_id")
    )
    first: dict[int, Image] = {}
    for img in images:
        if img.object_id not in first:
            first[img.object_id] = img
    return first


def _like_state(model_cls, object_ids: list[int], user) -> tuple[set[int], dict[int, int]]:
    if not object_ids:
        return set(), {}
    ct = ContentType.objects.get_for_model(model_cls)
    try:
        counts = (
            Like.objects.filter(content_type=ct, object_id__in=object_ids)
            .values("object_id")
            .annotate(c=Count("id"))
        )
        count_map = {row["object_id"]: row["c"] for row in counts}
    except OperationalError:
        # DB not migrated yet (e.g. missing catalog_like).
        return set(), {}

    liked_ids: set[int] = set()
    if user and getattr(user, "is_authenticated", False):
        try:
            liked_ids = set(
                Like.objects.filter(content_type=ct, object_id__in=object_ids, user=user).values_list(
                    "object_id", flat=True
                )
            )
        except OperationalError:
            return set(), count_map
    return liked_ids, count_map


def place_list(request):
    form = PlaceFilterForm(request.GET)
    form.is_valid()

    places = TouristPlace.objects.select_related("city", "city__region")
    q = (form.cleaned_data.get("q") or "").strip()
    region_id = form.cleaned_data.get("region")
    city_id = form.cleaned_data.get("city")

    if q:
        places = places.filter(
            Q(name__icontains=q)
            | Q(name_ru__icontains=q)
            | Q(name_en__icontains=q)
            | Q(short_description__icontains=q)
            | Q(short_description_ru__icontains=q)
            | Q(short_description_en__icontains=q)
            | Q(description__icontains=q)
            | Q(description_ru__icontains=q)
            | Q(description_en__icontains=q)
        )
    if region_id:
        places = places.filter(city__region_id=region_id)
    if city_id:
        places = places.filter(city_id=city_id)

    paginator = Paginator(places.order_by("name"), 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    object_ids = [p.id for p in page_obj.object_list]
    image_map = _first_image_map(TouristPlace, object_ids)
    liked_ids, like_counts = _like_state(TouristPlace, object_ids, request.user)
    basket_ids = _basket_state(TouristPlace, object_ids, request)
    for place in page_obj.object_list:
        place.cover_image = image_map.get(place.id)
        place.likes_count = like_counts.get(place.id, 0)

    return render(
        request,
        "places/list.html",
        {
            "form": form,
            "places": page_obj,
            "image_map": image_map,
            "liked_ids": liked_ids,
            "basket_ids": basket_ids,
            "like_counts": like_counts,
            "user_liked_places": liked_ids,
            "regions": Region.objects.all().order_by("name"),
            "cities": City.objects.all().order_by("name"),
        },
    )


def place_detail(request, pk: int):
    place = get_object_or_404(TouristPlace.objects.select_related("city", "city__region"), pk=pk)
    images = Image.objects.filter(
        content_type=ContentType.objects.get_for_model(TouristPlace), object_id=place.id
    ).order_by("sort_order", "id")
    reviews = (
        Review.objects.filter(
            content_type=ContentType.objects.get_for_model(TouristPlace),
            object_id=place.id,
            is_approved=True,
        )
        .select_related("user")
        .order_by("-created_at")[:20]
    )
    liked_ids, like_counts = _like_state(TouristPlace, [place.id], request.user)
    basket_ids = _basket_state(TouristPlace, [place.id], request)
    place.likes_count = like_counts.get(place.id, 0)
    query = quote_plus(place.map_query)
    return render(
        request,
        "places/detail.html",
        {
            "place": place,
            "images": images,
            "reviews": reviews,
            "map_embed_url": (
                f"https://www.google.com/maps?q={place.latitude},{place.longitude}&z=15&output=embed"
                if place.latitude is not None and place.longitude is not None
                else f"https://www.google.com/maps?q={query}&output=embed"
            ),
            "map_link_url": (
                f"https://www.google.com/maps?q={place.latitude},{place.longitude}"
                if place.latitude is not None and place.longitude is not None
                else f"https://www.google.com/maps?q={query}"
            ),
            "is_liked": (place.id in liked_ids),
            "liked": (place.id in liked_ids),
            "like_count": like_counts.get(place.id, 0),
            "in_basket": (place.id in basket_ids),
        },
    )


def accommodation_list(request):
    form = AccommodationFilterForm(request.GET)
    form.is_valid()

    qs = Accommodation.objects.select_related("city", "city__region")

    q = (form.cleaned_data.get("q") or "").strip()
    region_id = form.cleaned_data.get("region")
    city_id = form.cleaned_data.get("city")
    acc_type = (form.cleaned_data.get("type") or "").strip()
    min_price = form.cleaned_data.get("min_price")
    max_price = form.cleaned_data.get("max_price")

    if q:
        qs = qs.filter(
            Q(name__icontains=q)
            | Q(name_ru__icontains=q)
            | Q(name_en__icontains=q)
            | Q(short_description__icontains=q)
            | Q(short_description_ru__icontains=q)
            | Q(short_description_en__icontains=q)
            | Q(description__icontains=q)
            | Q(description_ru__icontains=q)
            | Q(description_en__icontains=q)
        )
    if region_id:
        qs = qs.filter(city__region_id=region_id)
    if city_id:
        qs = qs.filter(city_id=city_id)
    if acc_type:
        qs = qs.filter(type=acc_type)
    if min_price is not None:
        qs = qs.filter(price_per_night__gte=min_price)
    if max_price is not None:
        qs = qs.filter(price_per_night__lte=max_price)

    paginator = Paginator(qs.order_by("-created_at"), 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    object_ids = [a.id for a in page_obj.object_list]
    image_map = _first_image_map(Accommodation, object_ids)
    liked_ids, like_counts = _like_state(Accommodation, object_ids, request.user)
    basket_ids = _basket_state(Accommodation, object_ids, request)
    for acc in page_obj.object_list:
        acc.cover_image = image_map.get(acc.id)
        acc.likes_count = like_counts.get(acc.id, 0)
    return render(
        request,
        "accommodations/list.html",
        {
            "form": form,
            "accommodations": page_obj,
            "image_map": image_map,
            "liked_ids": liked_ids,
            "basket_ids": basket_ids,
            "like_counts": like_counts,
            "user_liked_accs": liked_ids,
            "regions": Region.objects.all().order_by("name"),
            "cities": City.objects.all().order_by("name"),
            "types": Accommodation.Type.choices,
            "accommodation_types": Accommodation.Type.choices,
        },
    )


def accommodation_detail(request, pk: int):
    accommodation = get_object_or_404(Accommodation.objects.select_related("city", "city__region"), pk=pk)
    images = Image.objects.filter(
        content_type=ContentType.objects.get_for_model(Accommodation),
        object_id=accommodation.id,
    ).order_by("sort_order", "id")
    reviews = (
        Review.objects.filter(
            content_type=ContentType.objects.get_for_model(Accommodation),
            object_id=accommodation.id,
            is_approved=True,
        )
        .select_related("user")
        .order_by("-created_at")[:20]
    )
    liked_ids, like_counts = _like_state(Accommodation, [accommodation.id], request.user)
    basket_ids = _basket_state(Accommodation, [accommodation.id], request)
    accommodation.likes_count = like_counts.get(accommodation.id, 0)
    return render(
        request,
        "accommodations/detail.html",
        {
            "accommodation": accommodation,
            "images": images,
            "reviews": reviews,
            "is_liked": (accommodation.id in liked_ids),
            "liked": (accommodation.id in liked_ids),
            "like_count": like_counts.get(accommodation.id, 0),
            "in_basket": (accommodation.id in basket_ids),
        },
    )


@login_required
@require_POST
def toggle_like(request):
    kind = (request.POST.get("kind") or "").strip().lower()
    object_id = request.POST.get("id")
    try:
        object_id_int = int(object_id)
    except Exception:
        return JsonResponse({"ok": False, "error": "invalid_id"}, status=400)

    if kind == "place":
        model_cls = TouristPlace
    elif kind == "accommodation":
        model_cls = Accommodation
    else:
        return JsonResponse({"ok": False, "error": "invalid_kind"}, status=400)

    ct = ContentType.objects.get_for_model(model_cls)
    try:
        qs = Like.objects.filter(user=request.user, content_type=ct, object_id=object_id_int)
        if qs.exists():
            qs.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, content_type=ct, object_id=object_id_int)
            liked = True

        count = Like.objects.filter(content_type=ct, object_id=object_id_int).count()
    except OperationalError:
        return JsonResponse({"ok": False, "error": "db_not_migrated"}, status=409)
    return JsonResponse({"ok": True, "liked": liked, "count": count})


@require_POST
def toggle_basket(request):
    kind = (request.POST.get("kind") or "").strip().lower()
    object_id = request.POST.get("id")
    try:
        object_id_int = int(object_id)
    except Exception:
        return JsonResponse({"ok": False, "error": "invalid_id"}, status=400)

    if kind not in {"place", "accommodation"}:
        return JsonResponse({"ok": False, "error": "invalid_kind"}, status=400)

    basket = list(request.session.get("basket_items", []))
    key = _basket_key(kind, object_id_int)
    if key in basket:
        basket.remove(key)
        in_basket = False
    else:
        basket.append(key)
        in_basket = True
    request.session["basket_items"] = basket
    request.session.modified = True
    return JsonResponse({"ok": True, "in_basket": in_basket, "count": len(basket)})


def basket(request):
    basket_items = request.session.get("basket_items", [])
    place_ids = []
    accommodation_ids = []
    for item in basket_items:
        try:
            kind, raw_id = item.split(":", 1)
            object_id = int(raw_id)
        except Exception:
            continue
        if kind == "place":
            place_ids.append(object_id)
        elif kind == "accommodation":
            accommodation_ids.append(object_id)

    places = list(TouristPlace.objects.filter(id__in=place_ids).select_related("city", "city__region"))
    accommodations = list(
        Accommodation.objects.filter(id__in=accommodation_ids).select_related("city", "city__region")
    )
    place_images = _first_image_map(TouristPlace, [p.id for p in places])
    accommodation_images = _first_image_map(Accommodation, [a.id for a in accommodations])
    items = []
    for place in places:
        place.item_type = "place"
        place.cover_image = place_images.get(place.id)
        items.append(place)
    for acc in accommodations:
        acc.item_type = "accommodation"
        acc.cover_image = accommodation_images.get(acc.id)
        items.append(acc)
    return render(request, "basket/basket.html", {"basket_items": items})


@require_POST
def toggle_basket_alias(request, kind: str, object_id: int):
    request.POST = request.POST.copy()
    request.POST["kind"] = kind
    request.POST["id"] = str(object_id)
    return toggle_basket(request)


@require_POST
def remove_from_basket(request, item_id: int, item_type: str):
    basket = list(request.session.get("basket_items", []))
    key = _basket_key(item_type, item_id)
    if key in basket:
        basket.remove(key)
        request.session["basket_items"] = basket
        request.session.modified = True
    return redirect("catalog:basket")


@login_required
@require_POST
def toggle_like_alias(request, kind: str, object_id: int):
    request.POST = request.POST.copy()
    request.POST["kind"] = kind
    request.POST["id"] = str(object_id)
    return toggle_like(request)
