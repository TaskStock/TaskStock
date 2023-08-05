from django.urls import path
from .views import *

urlpatterns = [
    path('add_todo/', add_todo), # /main/add_todo/
    path('delete_todo/<int:pk>/', delete_todo), # /main/delete_todo/1/
    path('check_todo/', check_todo), # /main/check_todo/
    path('', home), # /main/
    path('search/', search), # /main/search/
    path('settings/', settings), # /main/settings/

    # ajax 처리 url
    path('settings/update_introduce/', update_introduce), # /main/settings/update_introduce/
    path('settings/update_emailalarm/', update_emailalarm), # /main/settings/update_emailalarm/
    path('settings/update_hide/', update_hide), # /main/settings/update_hide/
    path('settings/update_language/', update_language), # /main/settings/update_language/
] 

