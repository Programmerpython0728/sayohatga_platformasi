from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from accounts import views as account_views
from bookings import views as booking_views
from catalog import views as catalog_views
from core import views as core_views
from core.sitemaps import SITEMAPS

places_patterns = ([
    path("", catalog_views.place_list, name="list"),
    path("<int:pk>/", catalog_views.place_detail, name="detail"),
    path("<int:object_id>/like/", catalog_views.toggle_like_alias, {"kind": "place"}, name="like"),
], "places")

accommodations_patterns = ([
    path("", catalog_views.accommodation_list, name="list"),
    path("<int:pk>/", catalog_views.accommodation_detail, name="detail"),
    path("<int:object_id>/like/", catalog_views.toggle_like_alias, {"kind": "accommodation"}, name="like"),
], "accommodations")

users_patterns = ([
    path("register/", account_views.register, name="register"),
    path("verify/", account_views.verify, name="verify"),
    path("resend-otp/", account_views.resend_otp, name="resend_otp"),
    path("login/", account_views.login_view, name="login"),
    path("logout/", account_views.logout_view, name="logout"),
    path("dashboard/", account_views.dashboard, name="dashboard"),
    path("profile/", account_views.profile, name="profile"),
    path("otp-help/", account_views.telegram_help, name="otp_help"),
], "users")

basket_patterns = ([
    path("", catalog_views.basket, name="view"),
    path("toggle/<str:kind>/<int:object_id>/", catalog_views.toggle_basket_alias, name="toggle"),
    path("remove/<int:item_id>/<str:item_type>/", catalog_views.remove_from_basket, name="remove"),
], "basket")

booking_alias_patterns = ([
    path("create/<int:accommodation_id>/", booking_views.create_booking, name="create"),
    path("cancel/<int:booking_id>/", booking_views.cancel_booking, name="cancel"),
], "bookings_alias")

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("uz/", core_views.language_root_redirect, {"code": "uz"}),
    path("ru/", core_views.language_root_redirect, {"code": "ru"}),
    path("en/", core_views.language_root_redirect, {"code": "en"}),
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    path("", core_views.home, name="home"),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("catalog/", include("catalog.urls")),
    path("bookings/", include("bookings.urls")),
    path("users/", include(users_patterns, namespace="users")),
    path("places/", include(places_patterns, namespace="places")),
    path("accommodations/", include(accommodations_patterns, namespace="accommodations")),
    path("basket/", include(basket_patterns, namespace="basket")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
