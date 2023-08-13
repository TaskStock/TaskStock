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
    path('settings/', settings), # /main/settings/name/
    path('settings/update_userinfo/', update_userinfo), # /main/settings/update_userinfo/
    path('category/', category), #/main/category/
    path('group/<int:pk>/', group), #/main/group/

    # 다른 유저의 상세 페이지
    path('profile/', profile), # /main/profile/
    path('alarm/', alarm), # /main/alarm/

    # ajax 처리 url
    path('settings/update_profile/', update_profile), # /main/settings/update_profile/
    path('settings/change_password/', change_password), # /main/settings/change_password/
    path('search/ajax/', search_ajax), # /main/search/ajax/
    path('follow_list/', follow_list), # /main/follow_list/

    # chart ajax
    path('chart_ajax/', chart_ajax), # /main/chart_ajax/

    # follow ajax
    path('follow/', follow), # /main/follow/

    # group ajax
    path('group/follow_group/', follow_group), # /main/follow_group/
    path('group/create_group/', create_group), # /main/create_group/
    path('group/delete_group/<int:pk>/', delete_group), # /main/delete_group/
    path('group/update_group/', update_group), # /main/update_group/
] 

