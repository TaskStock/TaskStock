from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Value)
admin.site.register(Category)
admin.site.register(Todo)
admin.site.register(Group)
admin.site.register(Badge)
admin.site.register(Alarm)
