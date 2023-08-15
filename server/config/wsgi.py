"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

#배포
import site

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 배포 과정에서 추가(manage.py의 위치를 추적)
site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

application = get_wsgi_application()
