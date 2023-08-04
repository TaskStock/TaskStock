from django.urls import path
from .views import *

urlpatterns = [
    path('add_todo/', add_todo),
    path('delete_todo', delete_todo),
    path('check_todo/', check_todo),
    path('', home),
    path('search/', search),
    path('settings/', settings),
]

