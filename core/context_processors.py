from __future__ import annotations

from django.core.cache import cache

from core.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from catalog.models import Region
from integrations.telegram import build_telegram_bot_url

NAV_REGIONS_CACHE_KEY = "nav_regions_v1"
NAV_REGIONS_TTL = 60 * 10  # 10 daqiqa


def get_nav_regions():
    """Navigatsiya uchun regionlar — har sahifada DB so'rovini oldini olish uchun cache."""
    regions = cache.get(NAV_REGIONS_CACHE_KEY)
    if regions is None:
        regions = list(Region.objects.all().order_by("name")[:12])
        cache.set(NAV_REGIONS_CACHE_KEY, regions, NAV_REGIONS_TTL)
    return regions


def nav_context(request):
    basket = request.session.get("basket_items", [])
    return {
        "nav_regions": get_nav_regions(),
        "telegram_bot_url": build_telegram_bot_url("sayohatga"),
        "current_site_language": getattr(request, "LANGUAGE_CODE", DEFAULT_LANGUAGE),
        "supported_site_languages": SUPPORTED_LANGUAGES,
        "basket_count": len(basket),
    }
