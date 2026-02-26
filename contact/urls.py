from django.urls import path
from .views import contact, submit_contact

urlpatterns = [
    path("", contact, name="contact"),
    path("submit/", submit_contact, name="contact_submit"),
]
