from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

def user_directory_path(instance, filename):
    #파일을 user_<id>/<filename>에 저장
    
    return f'profile/user_{instance.id}/{filename}'

class Group(models.Model):
    name = models.CharField(max_length=30)
    create_user = models.CharField(max_length=30, default= "")
    price = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name
    


class User(AbstractUser):
    combo = models.IntegerField(null=True, default=0)
    first_name=None
    last_name=None
    name = models.CharField(max_length=30, default="닉네임을 설정하세요")
    introduce = models.CharField(max_length=50, null=True, blank=True)
    email_alarm = models.BooleanField(null=True, default=False)
    img = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    tzinfo = models.CharField(max_length=50, default='Asia/Seoul')

    # false = public, true = private
    hide = models.BooleanField(null=True, default=False)

    LANGUAGE_CHOICES=(
        ('KR', '한국어'),
        ('EN', 'English'),
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, null=True, default='KR')

    # 팔로잉/팔로워
    # null=True를 넣을 수 없어 최소 한명을 설정해야하나?
    # 만약 그렇다면 자기자신으로 설정하여 해결
    # 추후에 오류 발생하면 생각
    # 검색 기능 완성 시 다시 개발
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

    # 그룹 기능을 위해 추가
    my_group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='user_set',null=True)

    def __str__(self):
        return self.username
    
# User 모델 객체가 생성될 때 실행할 함수
@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        Value.objects.create(
            user=instance,
            date=instance.date_joined,
            percentage=0,
            start=50000,
            end=50000,
            low=50000,
            high=50000,
        )

class Value(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='value_user')
    date = models.DateTimeField()
    percentage = models.FloatField()
    start = models.IntegerField()
    end = models.IntegerField(null=True, default=0)
    low = models.IntegerField(null=True, default=0)
    high = models.IntegerField(null=True, default=0)
    is_dummy = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.date} - {self.user.username}'


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_user')
    name = models.CharField(max_length=30)
    finish = models.BooleanField(default=False)
    memory = models.TextField(null=True)

class Todo(models.Model):
    value = models.ForeignKey(Value, on_delete=models.CASCADE, related_name='todo_value')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='todo_category', null=True)
    content = models.TextField()
    goal_check = models.BooleanField()
    level = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    finish_at = models.DateTimeField(null=True)


#Badge 모델
class Badge(models.Model):
    users = models.ManyToManyField(User, related_name="badges")
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    #배지 부여할 때
    #user.badges.add(some_badge)