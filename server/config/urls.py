from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',include('server.apps.task_account.urls')),
    path('main/', include('server.apps.main.urls')),
    path('social_login/',include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG == False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)