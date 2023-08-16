from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
import arrow 
from datetime import timedelta

# 비밀번호 변경 위한 라이브러리
from django.contrib.auth.hashers import check_password
from django.contrib import auth

from django.core.exceptions import ObjectDoesNotExist

from django.core import serializers


#스케줄링 관련 함수
def decrease_value(user, target_arrow):
    #사용자의 전날 value객체 가져오기
    value_object = get_value_for_date(user, target_arrow)  #get_value_for_date함수는 local arrow 받아야 함
    
    if not value_object:
        print('전날 접속 안해서 value 없는 사용자')
        return

    todos = Todo.objects.filter(value=value_object, goal_check=False)
    for todo in todos:
        value_object.end -= todo.level * 1000
        value_object.save()
        
    print('process_decrease 가치 감소 check 실행')
    
    



#시간대 설정
@csrf_exempt
def set_timezone(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_timezone = data.get('timezone')
        
        #현재 로그인한 사람의 timezone정보를 업데이트
        user = request.user
        user.tzinfo = user_timezone
        user.save()
        print(user.tzinfo)
        return JsonResponse({'status':'success'})
    return JsonResponse({'status':'fail'})

#사용자 timezone의 현재 날짜 얻기 *user_timezone = user.tzinfo
#사용자의 시간대를 기반으로 현재 날짜를 가져옴
def get_current_arrow(user_timezone):
    now = arrow.now(user_timezone)
    return now  # 현재 날짜와 시간을 반환

def utc_to_local(utc_arrow, user_timezone):
    local_time = utc_arrow.to(user_timezone)
    return local_time 

def local_to_utc(local_arrow):
    utc_arrow = local_arrow.to('UTC')
    return utc_arrow 



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
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('/main/')
    if target_user.is_superuser:
        return redirect('/main/')

    current_user=request.user
    if target_user == current_user:
        return redirect('/main/settings/')
    
    if target_user in current_user.followings.all():
        follow_text='UNFOLLOW'
    else:
        follow_text='FOLLOW'

    # home 로직 가져옴
    process_combo(target_user)
    value = get_value_for_date(target_user)
    
    if value is None:
        # 로그인 했을 때 value가 없는 경우
        value = createValue(target_user)
        
    todos = Todo.objects.filter(value=value)
    date_id = value.pk
    todos_levels_dict = {}
    for todo in todos:
        todos_levels_dict[todo.id] = todo.level

    todos_sub_dict = {}
    for todo in todos:
        todos_sub_dict[todo.pk] = 5 - todo.level
    
    ctx ={ 
        'user':current_user,
        'target_user':target_user,
        'follow_text':follow_text,
        'todos_levels_dict': todos_levels_dict,
        'date_id':date_id, 
        'todos':todos,
        'todos_sub_dict': todos_sub_dict,
    }
    return render(request, 'main/profile.html', context=ctx)

@csrf_exempt
def update_profile(request):
    type = request.POST.get("type")
    radio = request.POST.get("radio")

    user=request.user

    if type=="email_alarm":
        if radio=="alarm-set":
            radio_value=True
        elif radio=="alarm-reset":
            radio_value=False
        user.email_alarm=radio_value
    elif type=="security":
        if radio=="public":
            radio_value=False
        elif radio=="private":
            radio_value=True
        user.hide=radio_value
    elif type=="language":
        user.language=radio

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
            "username":user.username,
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
        try:
            value = Value.objects.get(user=user, date=arrow.now())
            percent = value.percentage
        except:
            percent = 0
        
        user_data={
            "username":user.username,
            "name":user.name,
            "introduce":user.introduce,
            "percent": percent,
            "img": user.img.url if user.img else '/static/img/blank-profile-picture.png',
            # 추후 필요한 필드 추가
        }
        users.append(user_data)

    return JsonResponse({"users": users})

# **주의점: target_datetime 줄거면 무조건 utc의 datetime으로 줘야함
def createValue(user, target_arrow=None):
    if not target_arrow:
        current_local_aroow = get_current_arrow(user.tzinfo).ceil('day')
        target_arrow = local_to_utc(current_local_aroow)
    
    # 최초 회원가입 시 value가 자동 생성되므로 last_value값이 없는 경우는 없음
    last_value = Value.objects.filter(user=user, date__lt=target_arrow.datetime).order_by('-date').first()

    percentage = 0
    start = end = low = high = last_value.end
    
    value = Value.objects.create(
        user=user,
        date=target_arrow.datetime,  
        percentage=percentage,
        start=start,
        end=end,
        low=low,
        high=high,  
    )
    # add_price(user)
    return value

# 이 곳에 그룹 주가 상승 함수를 추가할 생각


@csrf_exempt
def chart_ajax(request):
    day = int(request.POST.get("day"))
    username = request.POST.get("username")

    if username == "":
        target_user = request.user
    else:
        target_user = User.objects.get(username=username)

    dataset = values_for_chart(target_user, day)

    return JsonResponse({"dataset": dataset})

@csrf_exempt
def follow(request):
    buttonText = request.POST.get("buttonText")
    username = request.POST.get("username")

    target_user = User.objects.get(username=username)
    current_user = request.user

    if buttonText == "FOLLOW":
        current_user.followings.add(target_user)
        text="UNFOLLOW"
    elif buttonText == "UNFOLLOW":
        current_user.followings.remove(target_user)
        text="FOLLOW"

    return JsonResponse({"text": text})

# ---환희 작업---#
def home(request):
    current_user = request.user
    value = get_value_for_date(current_user)
    
    if value == None:
        #로그인 했을 때 value가 없는 경우 create
        value = createValue(current_user)
        print('home로딩하면서 createValue')
        
    elif value.is_dummy and not value.is_updated:
        #오늘의 데이터가 미리 만들어진 더미데이터면(add_todo, values_for_chart) 업데이트로 접근
        loacl_today_arrow = get_current_arrow(current_user.tzinfo)
        utc_today_arrow  = local_to_utc(loacl_today_arrow)
        
        #자기 이전 value까지만 정렬해서 가져와야 하기 때문에 date_lt 사용
        last_value = Value.objects.filter(user=current_user, date__lt=utc_today_arrow.datetime).order_by('-date').first()

        value.start = value.end = last_value.end
        value.low = last_value.end - value.low
        value.high = last_value.end + value.high
        value.is_updated = True
        value.save()
        
    
    todos = Todo.objects.filter(value=value)
    date_id = value.pk
    todos_levels_dict = {}
    for todo in todos:
        todos_levels_dict[todo.pk] = todo.level

    todos_sub_dict = {}
    for todo in todos:
        todos_sub_dict[todo.pk] = 5 - todo.level
    
    followings_len = current_user.followings.count()

    categorys = Category.objects.all()
    #today_value = get_value_for_date(current_user)
    
    process_badges(value)
    context = {
        'user': current_user,
        'todos_levels_dict': todos_levels_dict,
        'followings': followings_len,
        'date_id':date_id, 
        'todos':todos,
        'todos_sub_dict': todos_sub_dict,
        'percent': value.percentage,
        'categorys': categorys,
    }
    return render(request, 'main/home2.html', context)


#---세원 작업---#
@login_required
def update_userinfo(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('img')
        name = request.POST.get('name')
        introduce = request.POST.get('profile-description')

        #새 이미지가 제출되었을 경우, 이전 이미지를 삭제
        if image and user.img:
            old_image_path = user.img.path
            if os.path.isfile(old_image_path):
                os.remove(old_image_path)

        if image:
            user.img = image
        if name:
            user.name = name
        if introduce:
            user.introduce = introduce
            
        user.save()
    
        return redirect('/main/settings/')
    
    return JsonResponse({"result": False, "error": "GET요청이 들어옴"})


"""
user만 넣으면 오늘 날짜의 value 반환하고, user, target_date 넣으면 그날의 date에 해당하는 value 가져오는 함수
"""
#local_arrow 받자
def get_value_for_date(user, target_arrow=None):
    if not target_arrow:
        target_arrow = get_current_arrow(user.tzinfo)
    
    start_local_arrow = target_arrow.floor('day')
    end_local_arrow = target_arrow.ceil('day')
    
    start_utc_arrow = local_to_utc(start_local_arrow)
    end_utc_arrow = local_to_utc(end_local_arrow)
    
    try:    
        value_object = Value.objects.get(user=user, date__gte=start_utc_arrow.datetime, date__lte=end_utc_arrow.datetime)
        print('get_value_for_date try 실행:, 검색범위', start_utc_arrow,'부터',end_utc_arrow )
    except Value.DoesNotExist:
        value_object = None
        print('get_value_for_date Value가 검색 범위 내 없음, Value=None 반환')

    return value_object


@csrf_exempt
def click_date(request):
    # 자바스크립트에서 날짜를 전달한다
    date_str = request.POST.get('str')  # '8/21/2023' 브라우저의로컬 시간대 들어온다
    print('click_date date_str:',date_str)
    username = request.POST.get("username")
    
    if username == "":
        target_user = request.user
    else:
        target_user = User.objects.get(username=username)

    #date_str을 arrow 자료형으로 변환
    local_arrow_object = arrow.get(date_str, 'M/D/YYYY', tzinfo=target_user.tzinfo)
    # target_user의 타임존을 기반으로 local_datetime_object를 UTC로 변환
    local_arrow_start = local_arrow_object.floor('day') #자정
    local_arrow_end = local_arrow_object.ceil('day')    #23:59:59
    print('click_date local:', local_arrow_start, '부터',local_arrow_end)

    utc_arrow_start = local_to_utc(local_arrow_start)
    utc_arrow_end = local_to_utc(local_arrow_end)


    todos = []
    try:
        value = Value.objects.get(user=target_user, date__gte=utc_arrow_start.datetime, date__lte=utc_arrow_end.datetime)
        print('click_date try 실행:, 검색범위', utc_arrow_start,'부터',utc_arrow_end )
        todo_objects = Todo.objects.filter(value=value)
        
        for todo in todo_objects:
            # target_user의 timezone을 기반으로 utc datetime을 로컬 datetime으로 변환
            local_datetime = utc_to_local(local_arrow_object, target_user.tzinfo)
            category_object = todo.category
            if category_object == None:
                category_name = ''
            else:
                category_name = category_object.name

            todo_data = {
                'date_id': todo.value.pk,
                'content': todo.content,
                'goal_check': todo.goal_check,
                'id': todo.pk,
                'level': todo.level,
                'month': local_datetime.month,
                'date': local_datetime.day,
                'year': local_datetime.year,
                'category':category_name,

            }
            todos.append(todo_data)
            
    except Value.DoesNotExist:
        todos = []
        
    categorys = Category.objects.all()

    category_datas=[]

    for tmp in categorys:
        category_datas.append(tmp.name)

    return JsonResponse({'todos':todos, 'category_datas':category_datas})

"""
Todo 추가 하는 함수
할 일 추가 버튼 누름 -> 새로운 Todo객체 생성(ajax로 구현할 예정) -> high, low 업데이트
"""
@csrf_exempt
def add_todo(request):
    if request.method == 'POST':
        print('add_todo실행')
        req = json.loads(request.body)
        content = req['content']
        my_level = req['level']
        date_str = req['date_id']
        category_name = req['category']
        
        # 현재 user 객체 가져오기
        current_user = request.user
    
        # date_str을 사용자의 timezone을 고려해서 arrow로 객체로 변환(local)
        target_arrow = arrow.get(date_str, 'M/D/YYYY', tzinfo=current_user.tzinfo).ceil('day')
        
        print('add_todo local target_arrow:', target_arrow)
        # date 일치하는 value 객체 가져오기
        value = get_value_for_date(current_user, target_arrow)
        
        # value 없는 날 - 달력 연결 후 '완료' 버튼 누르면 객체 생성
        if value == None:
            value = Value.objects.create(
            user=current_user,
            date=local_to_utc(target_arrow).datetime,   #DB에는 UTC로 저장
            percentage=0,
            start=0,
            end=0,
            low=0,
            high=0,
            is_dummy = True,
            )
            print('add_todo에서 완료 눌렀을 때 value 없는 날이라 일단 0으로 다 박음, create된 datetime =', target_arrow )
            value = get_value_for_date(current_user, target_arrow)
        
        # 현재 user의 caregory 객체 가져오기
        try:
            category = Category.objects.get(user=current_user, name=category_name)
        except ObjectDoesNotExist:
            category = None

        #edit todo 에서 카테고리 수정할 수 있도록 모든 카테고리 객체 전달
        categorys = Category.objects.all()
        category_datas=[]

        for tmp in categorys:
            category_datas.append(tmp.name)
        
        # 투두 객체 생성
        Todo.objects.create(
            value=value,
            category=category,
            content=content,
            level=my_level,
            goal_check=False,
        )
        todo = Todo.objects.filter(value=value).last()
        todo_id = todo.pk
        
        target_value = todo.value   #todo에 연결된 value
        # tododp 연결된 value.high값 업데이트
        target_value.high += my_level * 1000
        
        # todo에 연결된 value.low값 업데이트
        target_value.low -= my_level * 1000
        target_value.save()
        
        
        #방금 만들어진 todo 가져오기/수정하거나 삭제해야할 것 같아서 걍 id로 보냄
        return JsonResponse({'date_id':value.id, 'todo_id':todo_id, 'my_level': my_level, 'content': content, 'category_datas':category_datas})


"""
Todo 삭제 하는 함수 
할 일 삭제 버튼 누름 -> todo 객체 삭제(ajax) -> high, low 업데이트
"""
@login_required
@csrf_exempt
def delete_todo(request, pk):
    if request.method == 'POST':
        req = json.loads(request.body)
        todo_id = req['todo_id']
        current_user = request.user
        
        todo = Todo.objects.get(pk=todo_id)     
        
        value = todo.value
        
        #todo 삭제하기 전 연결된 value의 high값 업데이트
        value.high -= 1000*todo.level
        #todo 삭제하기 전 연결된 value의 low값 업데이트
        value.low += 1000*todo.level
        
        #체크되어 있다면
        if todo.goal_check:
            value.end -= 1000*todo.level
        
        #저장
        value.save()
        #todo삭제
        todo.delete()
        
        #combo 변화 처리    
        my_combo = process_combo(current_user)
    
    return JsonResponse({'my_combo': my_combo, 'id':todo_id, 'd_id': value.id})
"""
Todo 업데이트 하는 함수
content, level 업데이트 -> value high, low 업데이트
"""

@login_required
@csrf_exempt
def update_todo(request, pk):
    if request.method == "POST":
        req = json.loads(request.body)
        todo_id = req['todo_id']
        updated_level = int(req['curr_level'])
        updated_content = req['curr_content']
        c_name = req['c_value']
        
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

            #category 설정
            try:
                category = Category.objects.get(user=request.user, name=c_name)
                todo.category=category
            except ObjectDoesNotExist:
                todo.category=None
            
            todo.save()
            todo.value.save()

    return JsonResponse({'t_id': todo_id, 'c_level': updated_level, 'c_content': updated_content})


"""
할일 완료에 체크 표시/해제 -> 가치 등락 계산 -> end, percentage 업데이트
"""
@login_required
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
        
        #status에 따라 goal_check와 value의 end값 업데이트
        if todo_status == 'True':
            todo.goal_check = True
            value.end += 1000*todo.level
        else:
            todo.goal_check = False
            value.end -= 1000*todo.level
        
        #value의 percentage값 업데이트 -> 소수점 둘째자리까지
        if value.start == 0:
            value.percentage = round((value.end - 50000)/50000 * 100, 2)
        else:
            value.percentage = round((value.end - value.start)/value.start *100, 2) 
            
        todo.save()
        value.save()
            
        #combo변화 처리
        my_combo = process_combo(current_user)
        todo_status = str(todo_status)
        #badge 처리
        return JsonResponse({'my_combo': my_combo, 'todo_status': todo_status, 't_id':todo.pk, 'percent':value.percentage})
        


"""
차트로 보낼 data준비하는 함수
"""
def arrow_to_date(arrow_obj):
    timestamp_milliseconds = int(arrow_obj.timestamp()) * 1000  # 초 단위 타임스탬프를 밀리초로 변환
    return timestamp_milliseconds


def values_for_chart(user, term):
    user_timezone = user.tzinfo

    current_local_arrow = get_current_arrow(user_timezone)
    #local_date의 자정으로 만들기
    start_local_arrow = current_local_arrow.ceil('day')
    #이 작업 안해줘서 db에서 두번 만듦

    # 사용자의 시간대를 기반으로 UTC arrow로 변환
    current_utc_arrow = local_to_utc(start_local_arrow)
    print('value_for_chart local utc arrow:', current_utc_arrow)
    start_utc_arrow = current_utc_arrow.shift(days=-term+1)
    next_utc_arrow = start_utc_arrow.shift(days=1)
    
    dummy_candidate = [start_utc_arrow, next_utc_arrow]
    print('value_for_chart dummy_candidate:', dummy_candidate)
    # DB에 존재하는 로컬 시간대 날짜들 가져오기
    range_values = Value.objects.filter(user=user, date__range=(start_utc_arrow.datetime, current_utc_arrow.datetime))
    value_datetimes =[value.date.date() for value in range_values]

    #더미데이터 처리(start_utc_datetime.date()하고 그 다음날이 db에 없으면 create)
    for candidate in dummy_candidate:
        if candidate.datetime.date() not in value_datetimes:
            Value.objects.create(
                user=user,
                date=candidate.datetime,
                percentage=0,
                start=0,
                end=0,
                high=0,
                low=0,
                is_dummy=True,
            )

    # 최종 데이터 다시 쿼리하기
    values = Value.objects.filter(user=user, date__range=(start_utc_arrow.datetime, current_utc_arrow.datetime))
    print('start:', start_utc_arrow.datetime)
    print('current:', current_utc_arrow.datetime)

    dataset = [[arrow_to_date(utc_to_local(arrow.get(value.date), user_timezone)), value.start, value.high, value.low, value.end] for value in values]
    print(dataset)
    
    return dataset
    

"""
combo처리하는 함수
"""
def process_combo(user):
    # 사용자의 시간대를 기반으로 현재 arrow을 가져옴
    current_local_arrow = get_current_arrow(user.tzinfo).ceil('day')
    # UTC로 변환
    current_utc_arrow = local_to_utc(current_local_arrow)
    
    # 오늘 UTC datetime 기준으로 조회
    values = Value.objects.filter(user=user, date__lte=current_utc_arrow.datetime).order_by('-date')

    # 역순으로 체크
    combo = 0
    previous_datetime = None

    for value in values:
        todos = Todo.objects.filter(value=value)
        success_day = any(todo.goal_check for todo in todos)
    
        # previous_datetime이 설정되어 있고 그 간격이 1 일 이상이거나 체크한 날이 아니면 반복문 탈출
        if previous_datetime and (previous_datetime - value.date > timedelta(days=1)) or not success_day:
            break
        
        combo += 1
        previous_datetime = value.date
        
    user.combo = combo
    user.save()
    
        
    return combo

def process_badges(value):
    user = value.user
    acquired_badges = user.badges.values_list('name', flat=True)
    
    #지금이라도 사야해
    if user.combo == 10 and "지금이라도 사야해" not in acquired_badges:
        badge_to_add = Badge.objects.get(name="지금이라도 사야해")
        user.badges.add(badge_to_add)

    #개미의 선택
    if value.end >= 100000 and '개미의 선택' not in acquired_badges:
        badge_to_add = Badge.objects.get(name='개미의 선택')
        user.badges.add(badge_to_add)
    
    #슈퍼 개미의 선택
    if value.end >= 200000 and '슈퍼 개미의 선택' not in acquired_badges:
        badge_to_add = Badge.objects.get(name='슈퍼 개미의 선택')
        user.badges.add(badge_to_add)
    
    #우주 개미의 선택
    if value.end >= 500000 and '우주 개미의 선택' not in acquired_badges:
        badge_to_add = Badge.objects.get(name='우주 개미의 선택')
        user.badges.add(badge_to_add)
    
    #화성 갈끄니까
    if value.end >= 2000000 and '화성 갈끄니까' not in acquired_badges:
        badge_to_add = Badge.objects.get(name='화성 갈끄니까')
        user.badges.add(badge_to_add)
    
    #콩콩
    if value.percentage == 22 and '콩콩' not in acquired_badges:
        badge_to_add = Badge.objects.get(name='콩콩')
        user.badges.add(badge_to_add)
    
    #콩콩
    if value.percentage == 100 and '1+1' not in acquired_badges:
        badge_to_add = Badge.objects.get(name='1+1')
        user.badges.add(badge_to_add)
        
        


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

def landing_page(request):
    return render(request, 'main/landing_page.html')

# def settings(request):
#     return render(request, 'main/settings.html')





# alarm
def alarm(request):
    return render(request, 'main/alarm.html')


# category
def category(request):
    current_user=request.user
    finish_categorys = Category.objects.filter(user=current_user, finish=True)
    not_finish_categorys = Category.objects.filter(user=current_user, finish=False)

    ctx = {
        'user': current_user,
        'finish_categorys': finish_categorys,
        'not_finish_categorys': not_finish_categorys,
    }

    return render(request, 'main/category.html', context=ctx)

# category ajax
@csrf_exempt
def create_category(request):
    input_name = request.POST.get('name')

    error_text=""
    if input_name=="":
        success=False
        error_text="이름을 입력해주세요."
    else:
        try:
            category=Category.objects.get(name=input_name)
            success=False
            error_text="이미 존재하는 이름입니다."
        except ObjectDoesNotExist:
            success=True
        
    category_data={}
    if success:
        category = Category.objects.create(
            user=request.user,
            name=input_name,
            finish=False,
        )
        category_data={
            'name':category.name,
            'pk':category.pk,
        }

    return JsonResponse({'success':success, 'category_data':category_data, 'error_text':error_text})

@csrf_exempt
def update_category(request):
    name = request.POST.get('name')
    pk = request.POST.get('pk')

    update_category = Category.objects.get(pk=pk)
    origin_name=update_category.name
        
    # category 이름이 겹치는지 확인
    try:
        category = Category.objects.get(name=name)
        # 겹친 이름이 자기 자신이라면
        if category.pk==int(pk):
            raise ObjectDoesNotExist
        error_text="이미 존재하는 이름입니다."
    # 겹치지 않은 경우
    except ObjectDoesNotExist:
        
        update_category.name=name
        update_category.save()
        error_text=""

    return JsonResponse({'error_text':error_text, 'origin_name':origin_name,})

@csrf_exempt
def delete_category(request):
    pk = request.POST.get('pk')
    
    category = Category.objects.get(pk=pk)

    category.delete()

    return JsonResponse({'success':True})

@csrf_exempt
def finish_category(request):
    isChecked = request.POST.get('isChecked')
    pk = request.POST.get('pk')

    category = Category.objects.get(pk=pk)

    name = category.name

    if isChecked=='true':
        category.finish=True
    else:
        category.finish=False

    category.save()

    return JsonResponse({'success':True, 'name':name})

@csrf_exempt
def click_category(request):
    pk = request.POST.get('pk')
    
    category = Category.objects.get(pk=pk)

    category_data={
        'name':category.name,
        'memory':category.memory,
    }

    return JsonResponse({'category_data':category_data})

@csrf_exempt
def update_memory(request):
    pk = request.POST.get('pk')
    memory = request.POST.get('memory')
    
    category = Category.objects.get(pk=pk)

    category.memory=memory
    category.save()

    return JsonResponse({'success':True})

# group
# URL 뒤의 pk값을 가져와 해당 그룹의 페이지를 보여줌.
def group(request,pk):
    # group = Group.objects.get(id=pk)
    users = group.user_set.all()  # 그룹에 연결된 사용자들을 가져옵니다.
    value_dic={}
    my_group = request.user.my_group

    # 내가 방장일 때만 수정, 삭제 버튼이 보이도록 함.
    if group.create_user == request.user.name:
        am_I_creator = True
    else:
        am_I_creator = False

    # 팔로잉 버튼을 내 그룹 유무에 따라 다르게 표시.
    if my_group == group:
        button_text ="DELETE GROUP"
    else:
        button_text = "ADD GROUP"    
    # value_dic에 사용자 이름과 해당 사용자의 value를 넣음.
    for user in users:
        value = get_value_for_date(user)
        if value is None:
            value_dic[user.name] = 0
        else:
            value_dic[user.name] = value.end


    context = {
        'group': group,
        'users': users,
        'value': value_dic,
        'button_text': button_text,
        'am_I_creator': am_I_creator,
        'users_length': len(users),
    }
    return render(request, 'main/group.html', context)



@csrf_exempt
def follow_group(request):
    buttonText = request.POST.get("group-button")
    group = request.POST.get("group")
    target_group = Group.objects.get(name=group)
    current_user = request.user
    text="오류"

    if buttonText == "ADD GROUP":
        current_user.my_group = target_group
        text="DELETE GROUP"
    elif buttonText =="DELETE GROUP":
        current_user.my_group = None
        text="ADD GROUP"

    current_user.save()

    return JsonResponse({'text': text})


def create_group(request):
    user = request.user
    if request.method == 'POST':
        content = request.POST.get("name")
        if user.my_group is None:
            #그룹이 없는 경우에만 그룹 생성
            Group.objects.create(
                name=content,
                price=0,
                create_user=user.name,
            )
            user.my_group = Group.objects.get(name=content)
            user.save()

            return JsonResponse({'result': 'Success'})
        
        else:
            #그룹이 있는 경우
            return JsonResponse({'result': 'Exist'})

def update_group(request):
    if request.method == 'POST':
        update_content = request.POST.get("update_name")
        group_name = request.POST.get("group_name")
        group = Group.objects.get(name=group_name)
        # 중복 검사
        if Group.objects.filter(name=update_content).exists():
            return JsonResponse({'result': 'Exist'})
        else:
            group.name = update_content
            group.save()
            return JsonResponse({'result': 'Success'})

def delete_group(request,pk):
    if request.method == 'POST':
        group = Group.objects.get(pk=pk)
        group.delete()
        
        return redirect('/main/search_group/')
    
# def add_price(user):
#     last_value=Value.objects.filter(user=user, is_dummy=False).order_by('-date').first()
#     my_group = user.my_group
#     if my_group is not None:
#         my_group.price += last_value.start - last_value.end
#         my_group.save()

#     return my_group.price

# search에 그룹 검색 기능 추가
# 그룹에 멤버가 0명이라면 삭제하기

# group search에 관한 함수
def search_group(request):
    groups = Group.objects.all().order_by('-price')
    currentu_user = request.user
    filtered_groups = groups
    my_group = currentu_user.my_group


    ctx = {
        'groups': groups,
        'filtered_groups': filtered_groups,
        'my_group': currentu_user.my_group,
    }

    return render(request, 'main/search_group.html',context=ctx)


@csrf_exempt
def search_group_ajax(request):
    search_contents = request.POST.get("textContent")

    if search_contents is not None:
        find_groups = Group.objects.filter(name__contains=search_contents)
    else:
        find_groups = Group.objects.all()

    groups=[]

    for group in find_groups:
        group_data={
            "name":group.name,
            "price":group.price,
            "create_user":group.create_user,
            "pk":group.pk,
            # 추후 필요한 필드 추가
        }
        groups.append(group_data)

    return JsonResponse({"groups": groups})

