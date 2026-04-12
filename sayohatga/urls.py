from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core import views as core_views

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("uz/", core_views.language_root_redirect, {"code": "uz"}),
    path("ru/", core_views.language_root_redirect, {"code": "ru"}),
    path("en/", core_views.language_root_redirect, {"code": "en"}),
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("catalog/", include("catalog.urls")),
    path("bookings/", include("bookings.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
