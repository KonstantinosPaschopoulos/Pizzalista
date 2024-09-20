from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("", views.contact_us, name="contact-us"),
]
