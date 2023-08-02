from django.db import models

# Create your models here.

# User 모델은 추후 로그인 기능 때 구현 예정

class Value(models.Model):
    # 이름, 점수, 아이디, 비밀번호, 이메일, 생일
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='value_user')

    date = models.DateTimeField(auto_created=True, auto_now_add=True)
    percentage = models.FloatField()
    start = models.IntegerField()
    end = models.IntegerField()
    low = models.IntegerField()
    high = models.IntegerField()
    combo = models.IntegerField(null=True, default=0)

class Todolist(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todolist_user')
    
    # tmp는 임시 필드, user필드 넣으면 뺴야함
    tmp = models.IntegerField(null=True, default=0)

class Todo(models.Model):
    value = models.ForeignKey(Value, on_delete=models.CASCADE, related_name='todo_value')
    todolist = models.ForeignKey(Todolist, on_delete=models.CASCADE, related_name='todo_todolist')
    content = models.TextField()
    goal_check = models.BooleanField()
    level = models.IntegerField()

    created_time = models.DateTimeField(auto_now_add=True)
    # datetime(2023, 8, 2, 12, 34, 56) 년, 월, 일, 시, 분, 초
    finish_time = models.DateTimeField(null=True)