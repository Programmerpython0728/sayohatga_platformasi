from __future__ import annotations

from django import template

from core.i18n import translate_text

register = template.Library()


@register.simple_tag(takes_context=True)
def t(context, text: str):
    request = context.get("request")
    lang = getattr(request, "LANGUAGE_CODE", "uz") if request else "uz"
    return translate_text(text, lang)

