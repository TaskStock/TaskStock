from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.utils import timezone

# 비밀번호 변경 위한 라이브러리
from django.contrib.auth.hashers import check_password
from django.contrib import auth

"""
사용자가 로그인 할 때마다 value객체 검증하고 사용자의 가치 update
할일 추가 함수
할일 삭제 함수
체크 상태에 따라 가치 계산하는 함수
난이도 변경에 따라 가치 계산하는 함수
할일 수정 함수
팔로잉 검색하는 함수
팔로우 검색하는 함수
전체 사람 중에 검색하는 함수
"""

# Create your views here.
# ---정근 작업---#

def settings(request):
    user=request.user
    # 한 유저가 다른 유저의 프로필을 방문했을 때의 경우도 설계해야함
    
    ctx ={ 
        'user':user,
    }
    return render(request, 'main/settings.html', context=ctx)

@csrf_exempt
def update_introduce(request):
    introduce = request.POST.get("proflie-description")

    user=request.user
    user.introduce=introduce
    user.save()

    return JsonResponse({"result": True})

@csrf_exempt
def update_emailalarm(request):
    emailalarm = request.POST.get("radio")

    if emailalarm=="alarm-set":
        alarm=True
    elif emailalarm=="alarm-reset":
        alarm=False

    user=request.user
    user.email_alarm=alarm
    user.save()

    return JsonResponse({"result": True})

@csrf_exempt
def update_hide(request):
    hiderange = request.POST.get("radio")

    if hiderange=="public":
        hide=False
    elif hiderange=="private":
        hide=True

    user=request.user
    user.hide=hide
    user.save()

    return JsonResponse({"result": True})

@csrf_exempt
def update_language(request):
    language = request.POST.get("radio")

    user=request.user
    user.language=language
    user.save()

    return JsonResponse({"result": True})

@csrf_exempt
def change_password(request):
    current_password = request.POST.get("current-password")

    user=request.user
    if user.is_authenticated:
        if check_password(current_password,user.password):
            new_password = request.POST.get("new-password")
            new_password_check = request.POST.get("new-password-check")
            if new_password == new_password_check:
                user.set_password(new_password)
                user.save()
                auth.login(request,user, backend='django.contrib.auth.backends.ModelBackend')
                result=0
            else:
                result=2
        else:
            result=1
    else:
        result=-1
        
    # result
    # 0 : 정상적으로 변경됨, 1 : 현재 비밀번호와 다름, 2 : 새로운 비밀번호 확인이 틀림
    return JsonResponse({"result": result})

def following_list(request):
    user=request.user
    followings = user.followings.all()

    ctx ={ 
        'followings':followings,
    }
    return render(request, 'main/settings.html', context=ctx)

def follower_list(request):
    user=request.user
    followers = user.followers.all()

    ctx ={ 
        'followers':followers,
    }
    return render(request, 'main/settings.html', context=ctx)

# ---환희 작업---#

def home(request):
    value = get_todayValue()
    todos = Todo.objects.filter(value=value)
    
    return render(request, 'main/home.html', {'date_id':value.id, 'todos':todos})

def hello(request):
    context = {
                
            }
    return render(request, 'base.html', context=context)

#---세원 작업---#

"""
오늘 06:00:00이랑 다음날 06:00:00까지의 value객체 가져오는 함수 
"""
from datetime import datetime, timedelta

def get_todayValue():
    # 현재 시간을 가져온 후, 오늘 날짜의 06:00:00으로 설정
    #today_date = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    today_date = timezone.now().replace(hour=6, minute=0, second=0, microsecond=0)
    # start_date는 오늘 날짜의 06:00:00
    start_date = today_date
    # end_date는 start_date에서 1일 후 (즉, 내일의 06:00:00)
    end_date = start_date + timezone.timedelta(days=1)
    # date__gte와 date__lt를 사용하여 해당 범위 내의 Value 객체 가져오기
    value_object = Value.objects.get(date__gte=start_date, date__lt=end_date)
    return value_object

"""
Todo 추가 하는 함수
할 일 추가 버튼 누름 -> 새로운 Todo객체 생성(ajax로 구현할 예정) -> high, low 업데이트
"""
@csrf_exempt
def add_todo(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        content = req['content']
        my_level = req['level']
        #현재 user 객체 가져오기
        current_user = request.user
        
        #date 일치하는 value 객체 가져오기
        value = get_todayValue()
        
        #현재 user의 todolist 객체 가져오기
        category = Category.objects.get(user=current_user)
        
        #투두 객체 생성
        Todo.objects.create(
            value = value,
            category=category,
            content=content,
            level=my_level,
            goal_check=False,
        )
        todo = Todo.objects.filter(value=value).last()
        todo_id = todo.pk
        
        #todo의 high값 업데이트
        value.low += my_level*1000
        
        #todo의 low값 업데이트
        value.high -= my_level*1000
        value.save()
        
        #방금 만들어진 todo 가져오기/수정하거나 삭제해야할 것 같아서 걍 id로 보냄

        return JsonResponse({'date_id':value.id, 'todo_id':todo_id, 'my_level': my_level, 'content': content})
"""
Todo 삭제 하는 함수
할 일 삭제 버튼 누름 -> todo 객체 삭제(ajax) -> high, low 업데이트
"""
@csrf_exempt
def delete_todo(request, pk):
    if request.method == 'POST':
        req = json.loads(request.body)
        todo_id = req['todo_id']
        
        todo = Todo.objects.get(pk=todo_id)
        #todo 삭제하기 전 연결된 value의 high값 업데이트
        # todo.value.high -= 1000*todo.level
        #todo 삭제하기 전 연결된 value의 low값 업데이트
        # todo.value.low += 1000*todo.level
        #저장
        # todo.value.save()
        #todo삭제
        todo.delete()
        value = get_todayValue()
        
    return JsonResponse({'id':todo_id, 'd_id': value.id})


"""
할일 완료에 체크 표시/해제 -> 가치 등락 계산 -> end, percentage 업데이트
"""
@csrf_exempt
def check_todo(request):
    if request.method == "POST":
        req = json.loads(request.body)
        todo_id = req['id']
        todo_status = req['status']
        
        #해당되는 Todo 객체 가져오기
        todo = Todo.objects.get(id=todo_id)
        #오늘의 value 가져오기
        value = todo.value
        
        #status에 따라 goal_check와 value의 end값 업데이트
        if todo_status == 'checked':
            todo.goal_check = True
            value.end = value.start + 1000*todo.level
        else:
            todo.goal_check = False
            value.end = value.start - 1000*todo.level
        
        #value의 percentage값 업데이트
        value.percentage = int((value.end-value.start)/value.start *100)
        if value.percentage > 0:
            color = 'blue'
        else:
            color = 'red'
            
        todo.save()
        value.save
        
        return JsonResponse({'color':color, 'value':value, 'todo':todo})


#---선우 작업---#
def search(request):
    return render(request, 'main/search.html')

# def settings(request):
#     return render(request, 'main/settings.html')
