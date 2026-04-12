from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("lang/<str:code>/", views.set_site_language, name="set_site_language"),
]
