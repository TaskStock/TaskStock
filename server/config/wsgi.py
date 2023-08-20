"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

import site

from django.core.wsgi import get_wsgi_application

from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# 추가
site.addsitedir(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

application = Sentry(get_wsgi_application())

from server.apps.main.jobs import scheduler
