from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import pytz
from datetime import timedelta, datetime
from django.db import transaction


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

# 내가 아닌 다른 유저의 프로필을 보는 함수
def profile(request):
    username=request.GET.get('username')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('/main/')
    if user.is_superuser:
        return redirect('/main/')

    current_user=request.user
    if user == current_user:
        return redirect('/main/settings/')
    
    ctx ={ 
        'user':user,
    }
    return render(request, 'main/profile.html', context=ctx)

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
    elif request.POST.get("type")=="following_search":
        follow_list = current_user.followings.filter(name__contains=request.POST.get("searchtext"))
    elif request.POST.get("type")=="follower_search":
        follow_list = current_user.followers.filter(name__contains=request.POST.get("searchtext"))

    users=[]

    for user in follow_list:
        user_data={
            "username":user.username,
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
    start = end = low = high = last_value.end
    value = Value.objects.create(
        user=user,
        date=timezone.now(),
        percentage=percentage,
        start=start,
        end=end,
        low=low,
        high=high,
    )
    return value

@csrf_exempt
def chart_ajax(request):
    day = int(request.POST.get("day"))
    username = request.POST.get("username")

    target_user = User.objects.get(username=username)

    dataset = values_for_chart(target_user, day)

    return JsonResponse({"dataset": dataset})

# ---환희 작업---#

def home(request):
    current_user = request.user
    process_combo(current_user)
    value = get_value_for_date(current_user)
    
    if value is None:
        # 로그인 했을 때 value가 없는 경우
        value = createValue(current_user)
        
    todos = Todo.objects.filter(value=value)
    date_id = value.pk
    todos_levels_dict = {}
    for todo in todos:
        todos_levels_dict[todo.id] = todo.level

    todos_sub_dict = {}
    for todo in todos:
        todos_sub_dict[todo.pk] = 5 - todo.level
    
    # 데이터
    # dataset = values_for_chart(current_user, 7)
    
    followings_len = current_user.followings.count()
    context = {
        'user': current_user,
        'followings': followings_len,
        'todos_levels_dict': todos_levels_dict,
        'date_id':date_id, 
        'todos':todos,
        'todos_sub_dict': todos_sub_dict,
    }
    return render(request, 'main/home2.html', context)


#---세원 작업---#
#시간 디버깅용 함수
def time():
    print('utc시간: ', timezone.now())   #UTC 기준으로 가져옴
    print('kst시간: ', timezone.localtime()) #Asia/Seoul 기준으로 가져옴


"""
user만 넣으면 오늘 날짜의 value 반환하고, user, target_date 넣으면 그날의 date 가져오는 함수
"""
def get_value_for_date(user, target_date=None):
    if not target_date:
        target_date = timezone.localtime(timezone.now()).date()
    
    try:    
        value_object = Value.objects.get(user=user, date=target_date)
    except:
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
        value = get_value_for_date(current_user)
        
        #달력 연결 대비
        # if value is None:
        #     createValue(current_user)
            
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
        value.high += my_level*1000
        
        #todo의 low값 업데이트
        value.low -= my_level*1000
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
        current_user = request.user
        value = get_value_for_date(current_user)
        
        with transaction.atomic():
            todo = Todo.objects.get(value=value, pk=todo_id)
            #todo 삭제하기 전 연결된 value의 high값 업데이트
            todo.value.high -= 1000*todo.level
            #todo 삭제하기 전 연결된 value의 low값 업데이트
            todo.value.low += 1000*todo.level
            #저장
            todo.value.save()
            #todo삭제
            todo.delete()
        
        #combo 변화 처리    
        process_combo(current_user)
            
    return JsonResponse({'id':todo_id, 'd_id': value.id})
"""
Todo 업데이트 하는 함수
content, level 업데이트 -> value high, low 업데이트
"""
@csrf_exempt
def update_todo(request, pk):
    if request.method == "POST":
        req = json.loads(request.body)
        todo_id = req['todo_id']
        updated_level = int(req['curr_level'])
        updated_content = req['curr_content']
        
        with transaction.atomic():
            todo = Todo.objects.get(pk=todo_id)
            #value의 high, low add_todo실행 이전 값으로 돌리기 
            todo.value.high -= todo.level * 1000
            todo.value.low += todo.level *1000
            
            #todo 내용 update
            todo.level = updated_level
            todo.content = updated_content
            
            #value의 high, low updated_level 반영해서 다시 넣기
            todo.value.high += updated_level * 1000
            todo.value.low -= updated_level * 1000
            
            todo.save()
            todo.value.save()

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
        
        current_user = request.user
        #오늘의 value 가져오기
        value = get_value_for_date(current_user)
        
        #해당되는 todo 가져오기
        todo = Todo.objects.get(pk=todo_id)
        
        with transaction.atomic():
        #status에 따라 goal_check와 value의 end값 업데이트
            if todo_status == 'True':
                todo.goal_check = True
                value.end += 1000*todo.level
            else:
                todo.goal_check = False
                value.end -= 1000*todo.level
            
            #value의 percentage값 업데이트 -> 소수점 둘째자리까지
            if value.start == 0:
                value.percentage = int((value.end - 50000)/50000 * 100)
            else:
                value.percentage = int((value.end-value.start)/value.start *100)
                
            if value.percentage > 0:
                color = 'red'
            else:
                color = 'blue'
            
            todo.save()
            value.save()
            
        #combo변화 처리
        process_combo(current_user)
        todo_status = str(todo_status)
        return JsonResponse({'color':color, 'todo_status': todo_status, 't_id':todo.pk})
        


"""
차트로 보낼 data준비하는 함수
"""
#유저의 최초회원가입 날짜로부터 경과한 날짜 반환하는 함수
# def days_since_joined(user):
#     delta = timezone.now() - user.date_joined
    
#     return delta.days   #int자료형으로 반환

def date_to_timestamp(date_obj):
    
    return int(datetime.combine(date_obj, datetime.min.time()).timestamp() * 1000)

def values_for_chart(user, term):
    kst = pytz.timezone('Asia/Seoul')
    kst_date = timezone.now().astimezone(kst).date()
    start_date = kst_date - timedelta(days=term-1)
    
    #db에 존재하는 date들 가져오기
    range_values =  Value.objects.filter(user=user, date__range=(start_date, kst_date))
    value_dates = set(range_values.values_list('date', flat=True))
    
    #첫 시작 날짜에 대한 더미데이터 처리
    date_list = [start_date, start_date + timedelta(days=1)]
    for date in date_list:
        if date not in value_dates:
            Value.objects.create(
                user=user,
                date=date,
                percentage=0,
                start=0,
                end=0,
                high=0,
                low=0,
            )

    #최종 데이터 다시 쿼리하기
    values = Value.objects.filter(user=user, date__range=(start_date, kst_date))
    
    dataset = [[date_to_timestamp(value.date), value.start, value.high, value.low, value.end] for value in values]
    
    return dataset
    

"""
combo처리하는 함수
"""
def process_combo(user):
    #전체 기간의 value들을 내림차순으로 가져와서 goal_check=True인 todo가 있는지 확인
    #date가 연속적이지 않을때까지 combo += 1
    #goal_check=False인 todo가 나올때까지 combo += 1
    #두 조건 and로 연결
    values = Value.objects.filter(user=user).order_by('-date')
    
    #역순으로 체크
    combo = 0
    previous_date = None

    for value in values:
        todos = Todo.objects.filter(value=value)
        
        checked_day = any(todo.goal_check for todo in todos)
        
        if (previous_date and previous_date - value.date > timedelta(days=1)) or not checked_day:
            break
        print('previous_date:', previous_date)
        print('valid_date:', value.date)
        
        combo += 1
        previous_date = value.date
        
    user.combo = combo
    user.save()
        
    return
#---선우 작업---#

def search(request):
    current_user = request.user
    followings_len = current_user.followings.count()
    
    search_content = request.GET.get('search_content','')
    users = User.objects.all()
    filtered_users = users
    if search_content:
        filtered_users = User.objects.all().filter(name__contains=search_content)

    ctx = {
        'users': users,
        'followings': followings_len,
        'filtered_users': filtered_users,
    }

    return render(request, 'main/search.html',context=ctx)

def landing_page(request):
    return render(request, 'main/landing_page.html')

# def settings(request):
#     return render(request, 'main/settings.html')

