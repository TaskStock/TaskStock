from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('server.apps.account.urls')),
    path('main/', include('server.apps.main.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG == False:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)