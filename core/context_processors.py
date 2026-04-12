from __future__ import annotations

from django.conf import settings

from core.i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES
from catalog.models import Region


def nav_context(request):
    basket = request.session.get("basket_items", [])
    return {
        "nav_regions": Region.objects.all().order_by("name")[:12],
        "telegram_bot_url": getattr(settings, "TELEGRAM_BOT_URL", ""),
        "current_site_language": getattr(request, "LANGUAGE_CODE", DEFAULT_LANGUAGE),
        "supported_site_languages": SUPPORTED_LANGUAGES,
        "basket_count": len(basket),
    }
