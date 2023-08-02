from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('signup/step1/', signup1),
    path('signup/step2/', signup2),
]
