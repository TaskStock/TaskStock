from django.db import models
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
import pytz

def user_directory_path(instance, filename):
    #파일을 user_<id>/<filename>에 저장
    
    return f'profile/user_{instance.id}/{filename}'

class Group(models.Model):
    name = models.CharField(max_length=30)
    create_user = models.CharField(max_length=30, default= "")
    price = models.IntegerField(null=True, default=0)
    password = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.name
    


class User(AbstractUser):
    combo = models.IntegerField(null=True, default=0)
    first_name=None
    last_name=None
    name = models.CharField(max_length=30, default="관리자")
    introduce = models.CharField(max_length=50, null=True, blank=True)
    email_alarm = models.BooleanField(null=True, default=False)
    img = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    tzinfo = models.CharField(max_length=50, default='Asia/Seoul')
    todo_cnt = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)
    custom_active = models.BooleanField(default=False)


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
    now_kst = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Seoul'))

    if now_kst.hour < 9:
        final_time = (now_kst - timedelta(days=1)).replace(hour=14, minute=59, second=59).replace(tzinfo=pytz.utc)
    else:
        final_time = now_kst.replace(hour=14, minute=59, second=59).replace(tzinfo=pytz.utc)

    if created:
        Value.objects.create(
            user=instance,
            #오늘이 한국시간 기준 8월 16일 이면 utc 8월 15일 15:00:00 부터 8월 16일 14:59:59 조회함 
            date=final_time,
            percentage=0,
            start=50000,
            end=50000,
            low=50000,
            high=50000,
            is_updated=True,
        )
        Alarm.objects.create(
            user=instance,
            content=instance.name+" 님의 가입을 축하드립니다! 주가 상승을 기원하겠습니다.",
            alarm_type="account",
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
    is_updated = models.BooleanField(default=False)
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
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

    #배지 부여할 때
    #user.badges.add(some_badge)


class Alarm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alarm_user')
    content = models.TextField()
    img = models.TextField(null=True, default="base_img")
    alarm_type = models.CharField(max_length=30)
    is_read = models.BooleanField(null=True, default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    # 유저
    # 내용
    # 이미지 경로
    # 알림 유형 ( account, follow, badge, category, group, ranking )
    # 읽음 여부

    # 생성 일자