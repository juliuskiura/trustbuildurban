from django.urls import path
from .views import (
    available_homes,
    property_detail_test,
    property_detail,
    submit_showing_request,
    submit_property_offer,
)

urlpatterns = [
  
    path("<slug:slug>/", property_detail, name="property_detail"),
    path("api/submit-showing/", submit_showing_request, name="submit_showing_request"),
    path("api/submit-offer/", submit_property_offer, name="submit_property_offer"),
]
