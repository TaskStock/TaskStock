from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('signup/step1/', signup1),
    path('signup/step2/', signup2),
    path('email_validation/', email_validation),
]
