from django.urls import path

from . import views

app_name = "maps"
urlpatterns = [
    path("", views.pizzeria_map_view, name="map-index"),
]
