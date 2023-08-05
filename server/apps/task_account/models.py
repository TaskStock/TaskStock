from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name=None
    last_name=None
    name = models.CharField(max_length=30, default="닉네임을 설정하세요")
    introduce = models.CharField(max_length=50, null=True, blank=True)
    email_alarm = models.BooleanField(null=True, default=False)

    # false = public, true = private
    hide = models.BooleanField(null=True, default=False)

    LANGUAGE_CHOICES=(
        ('KR', '한국어'),
        ('EN', 'English'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=True, default='KR')

    def __str__(self):
        return self.username

class Value(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='value_user')
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    percentage = models.FloatField()
    start = models.IntegerField()
    end = models.IntegerField(null=True, default=0)
    low = models.IntegerField(null=True, default=0)
    high = models.IntegerField(null=True, default=0)
    combo = models.IntegerField(null=True, default=0)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_user')

class Todo(models.Model):
    value = models.ForeignKey(Value, on_delete=models.CASCADE, related_name='todo_value')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='todo_category', null=True)
    content = models.TextField()
    goal_check = models.BooleanField()
    level = models.IntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True)