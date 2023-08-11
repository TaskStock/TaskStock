from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import server.apps.main.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('server.apps.task_account.urls')),
    path('', server.apps.main.views.landing_page),
    path('main/', include('server.apps.main.urls')),
    path('social_login/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
