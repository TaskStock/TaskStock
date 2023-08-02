from django.urls import path
from .views import *

urlpatterns = [
    path('', hello),
    path('add_task/', add_todo),
    path('task_complete/', complete_task),
]

