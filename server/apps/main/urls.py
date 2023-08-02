from django.urls import path
from .views import *

urlpatterns = [
    path('', hello),
    path('task_complete/', task_compelete),
]

