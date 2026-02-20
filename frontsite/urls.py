from django.urls import path
from .views import available_homes, index

urlpatterns = [
    path('', index, name='index'),
    path('available/', available_homes, name='available_homes')

]