from __future__ import annotations

from django.utils import translation

from .i18n import DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES


class SessionLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        code = request.session.get("site_language") or request.COOKIES.get("site_language") or DEFAULT_LANGUAGE
        if code not in SUPPORTED_LANGUAGES:
            code = DEFAULT_LANGUAGE
        translation.activate(code)
        request.LANGUAGE_CODE = code
        response = self.get_response(request)
        translation.deactivate()
        return response

