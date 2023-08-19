from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()

@register.filter
def time_since(value):
    now = timezone.now()
    diff = now - value

    if diff < timedelta(minutes=1):
        return f"{diff.seconds}초 전"
    elif diff < timedelta(hours=1):
        return f"{diff.seconds // 60}분 전"
    elif diff < timedelta(days=1):
        return f"{diff.seconds // 3600}시간 전"
    else:
        return value.strftime('%Y년 %m월 %d일')
