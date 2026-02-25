from django.urls import path
from .views import available_homes, property_detail_test, property_detail

urlpatterns = [
    path("", available_homes, name="available_homes"),
    path("test-design/", property_detail_test, name="property_detail_test"),
    path("<slug:slug>/", property_detail, name="property_detail"),
]
