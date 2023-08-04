from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name=None
    last_name=None
    name = models.CharField(max_length=30, default="닉네임")

    def __str__(self):
        return self.username

class Value(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='value_user')
    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    percentage = models.FloatField()
    start = models.IntegerField()
    end = models.IntegerField(null=True)
    low = models.IntegerField(null=True)
    high = models.IntegerField(null=True)
    combo = models.IntegerField(null=True, default=0)

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_user')

class Todo(models.Model):
    value = models.ForeignKey(Value, on_delete=models.CASCADE, related_name='todo_value')
    todolist = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='todo_category')
    content = models.TextField()
    goal_check = models.BooleanField()
    level = models.IntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(null=True)