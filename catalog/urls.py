from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("places/", views.place_list, name="place_list"),
    path("places/<int:pk>/", views.place_detail, name="place_detail"),
    path("accommodations/", views.accommodation_list, name="accommodation_list"),
    path("accommodations/<int:pk>/", views.accommodation_detail, name="accommodation_detail"),
    path("like/toggle/", views.toggle_like, name="toggle_like"),
    path("basket/", views.basket, name="basket"),
    path("basket/toggle/", views.toggle_basket, name="toggle_basket"),
]
