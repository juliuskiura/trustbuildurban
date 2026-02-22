from django.urls import path
from .views import available_homes

urlpatterns = [
    path("", available_homes, name="available_homes"),
]
