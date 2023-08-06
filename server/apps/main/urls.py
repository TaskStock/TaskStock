from django.urls import path
from .views import *

urlpatterns = [
    path('add_todo/', add_todo), # /main/add_todo/
    path('delete_todo/<int:pk>/', delete_todo), # /main/delete_todo/1/
    path('check_todo/', check_todo), # /main/check_todo/
    path('', home), # /main/
    path('search/', search), # /main/search/
    path('search_users/', search_users), # /main/search/
    path('settings/', settings), # /main/settings/
] 

