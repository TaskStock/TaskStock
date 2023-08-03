from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    path('search/', search),
    path('settings/', settings),
]
