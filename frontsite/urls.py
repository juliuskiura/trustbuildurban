from django.urls import path
from .views import about, available_homes, blog, guide, index, portfolio, process, services

urlpatterns = [
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("blog/", blog, name="blog"),
    path("guide/", guide, name="guide"),
    path("portfolio/", portfolio, name="portfolio"),
    path("process/", process, name="process"),
    path("services/", services, name="services"),
    path("available/", available_homes, name="available_homes"),
]
