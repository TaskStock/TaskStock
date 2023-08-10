from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login),
    path('logout/', logout),
    path('signup/step1/', signup1),
    path('signup/step2/', signup2),
    path('find_password/', find_password),

    # ajax
    path('email_validation/', email_validation),
    path('check_id/', check_id),
    path('activate/<str:username>/', activate_account),
]
