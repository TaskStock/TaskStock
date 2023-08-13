from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Django 설정 모듈을 지정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('server')

# Django settings에서 Celery 설정을 가져옵니다.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 태스크 모듈을 자동으로 등록합니다.
app.autodiscover_tasks()
