from django.urls import path
from .views import *

urlpatterns = [
    path('add_todo/', add_todo), # /main/add_todo/
    path('delete_todo/<int:pk>/', delete_todo), # /main/delete_todo/1/
    path('update_todo/<int:pk>/', update_todo), # /main/update_todo/1/
    path('check_todo/<int:pk>/', check_todo), # /main/check_todo/1/
    path('click_date/', click_date), # /main/click_date/
    path('', home), # /main/
    path('search/', search), # /main/search/
    path('settings/', settings), # /main/settings/
    path('settings/update_profile/', update_profile), # /main/settings/update_profile/
    
    # 다른 유저의 상세 페이지
    path('profile/', profile), # /main/profile/
    path('alarm/', alarm), # /main/alarm/

    # ajax 처리 url

    path('settings/update_profile/', update_profile), # /main/settings/update_profile/

    # path('settings/update_emailalarm/', update_emailalarm), # /main/settings/update_emailalarm/
    # path('settings/update_hide/', update_hide), # /main/settings/update_hide/
    # path('settings/update_language/', update_language), # /main/settings/update_language/

    path('settings/change_password/', change_password), # /main/settings/change_password/
    path('search/ajax/', search_ajax), # /main/search/ajax/
    path('follow_list/', follow_list), # /main/follow_list/

    # chart ajax
    path('chart_ajax/', chart_ajax), # /main/chart_ajax/

    # follow ajax
    path('follow/', follow), # /main/follow/
] 

