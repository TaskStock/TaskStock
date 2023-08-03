from django.urls import path
from .views import *

urlpatterns = [
    path('add_task/', add_todo),
    path('check_task/', check_task),
    path('', home),
    path('search/', search),
]

