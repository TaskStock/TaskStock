from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import pytz


# 비밀번호 변경 위한 라이브러리
from django.contrib.auth.hashers import check_password
from django.contrib import auth

from django.core.exceptions import ObjectDoesNotExist

from django.core import serializers

"""
사용자가 로그인 할 때마다 value객체 검증하고 사용자의 가치 update //만드는 중
할일 추가 함수 //만듬
할일 삭제 함수 //만듬
체크 상태에 따라 가치 계산하는 함수 //만듬
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

@csrf_exempt
def search_ajax(request):
    search_content = request.POST.get("text")

    if search_content is not None:
        find_users = User.objects.filter(name__contains=search_content).exclude(pk=request.user.pk)
    else:
        find_users = User.objects.all().exclude(pk=request.user.pk)

    users=[]

    for user in find_users:
        user_data={
            "name":user.name,
            "introduce":user.introduce,
            # 추후 필요한 필드 추가
        }
        users.append(user_data)

    return JsonResponse({"users": users})

@csrf_exempt
def follow_list(request):
    current_user=request.user

    if request.POST.get("type")=="following":
        follow_list = current_user.followings.all()
    elif request.POST.get("type")=="follower":
        follow_list = current_user.followers.all()

    users=[]

    for user in follow_list:
        user_data={
            "name":user.name,
            "introduce":user.introduce,
            # 추후 필요한 필드 추가
        }
        users.append(user_data)

    return JsonResponse({"users": users})

def createValue(user):
    last_value=Value.objects.filter(user=user).order_by('-date').first()
    # 마지막 생성된 value 기준으로 새로운 value 값들을 계산하는 로직 필요
    # 최초 회원가입 시 value가 자동 생성되므로 last_value값이 없는 경우는 없음
    percentage=0
    start=50000
    end=0
    low=0
    high=0
    combo=0
    value = Value.objects.create(
        user=user,
        date=timezone.now(),
        percentage=percentage,
        start=start,
        end=end,
        low=low,
        high=high,
        combo=combo,
    )
    return value

# ---환희 작업---#

def home(request):
    current_user = request.user
    value = get_todayValue(current_user)
    if value is None:
        # 로그인 했을 때 value가 없는 경우
        value = createValue(request.user)
        
    todos = Todo.objects.filter(value=value)
    date_id = value.pk

    todos_levels_dict = {}
    for todo in todos:
        todos_levels_dict[todo.id] = todo.level

    todos_sub_dict = {}
    for todo in todos:
        todos_sub_dict[todo.pk] = 5 - todo.level

    
    #데이터
    # dataset = values_for_chart(current_user, 7)
    context = {
        'todos_levels_dict': todos_levels_dict,
        'date_id':date_id, 
        'todos':todos,
        'todos_sub_dict': todos_sub_dict,
    }
    return render(request, 'main/home2.html', context)


#---세원 작업---#
#시간 디버깅용 함수
def time():
    print(timezone.now())   #UTC 기준으로 가져옴
    print(timezone.localtime()) #Asia/Seoul 기준으로 가져옴


"""
오늘 자정이랑 다음날 자정까지의 value객체 가져오는 함수 
"""
def get_todayValue(user):
    # 현재 시간을 가져온 후, 한국 기준오늘 날짜의 00:00:00으로 설정
    today_date = timezone.localtime(timezone.now()).replace(hour=0, minute=0, second=0, microsecond=0)
    print(today_date)
    # start_date는 오늘 날짜의 자정(DB에 UTC 기준으로 저장되어 있으니까 UTC로 변환)
    start_date = today_date.astimezone(pytz.UTC)
    print(start_date)
    # end_date는 start_date에서 1일 후 (UTC로 변환)
    end_date = start_date + timezone.timedelta(days=1)
    print(end_date)
    # date__gte와 date__lt를 사용하여 해당 범위 내의 Value 객체 가져오기
    try:
        value_object = Value.objects.get(user=user, date__gte=start_date, date__lt=end_date)
    except ObjectDoesNotExist:
        value_object = None
        
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
        value = get_todayValue(current_user)
        
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
        todo.value.high -= 1000*todo.level
        #todo 삭제하기 전 연결된 value의 low값 업데이트
        todo.value.low += 1000*todo.level
        #저장
        todo.value.save()
        #todo삭제
        todo.delete()
        current_user=request.user
        value = get_todayValue(current_user)
        
    return JsonResponse({'id':todo_id, 'd_id': value.id})

@csrf_exempt
def update_todo(request, pk):
    if request.method == "POST":
        req = json.loads(request.body)
        todo_id = req['todo_id']
        updated_level = req['curr_level']
        updated_content = req['curr_content']
        todo = Todo.objects.get(pk=todo_id)
        todo.level = updated_level
        todo.content = updated_content

        todo.save()

    return JsonResponse({'t_id': todo_id, 'c_level': updated_level, 'c_content': updated_content})




"""
할일 완료에 체크 표시/해제 -> 가치 등락 계산 -> end, percentage 업데이트
"""
@csrf_exempt
def check_todo(request, pk):
    if request.method == "POST":
        req = json.loads(request.body)
        todo_id = req['todo_id']
        todo_status = req['status']
        
        #해당되는 Todo 객체 가져오기
        todo = Todo.objects.get(pk=todo_id)
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
        value.save()
        
        return JsonResponse({'color':color, 'value':value, 'todo':todo})




#---선우 작업---#

def search(request):
    search_content = request.GET.get('search_content','')
    users = User.objects.all()
    filtered_users = users
    if search_content:
        filtered_users = User.objects.all().filter(name__contains=search_content)

    ctx = {
        'users': users,
        'filtered_users': filtered_users,
    }

    return render(request, 'main/search.html',context=ctx)

# def settings(request):
#     return render(request, 'main/settings.html')

