from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import pytz
from datetime import timedelta, datetime
from django.db import transaction
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings



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
        target_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('/main/')
    if target_user.is_superuser:
        return redirect('/main/')

    current_user=request.user
    if target_user == current_user:
        return redirect('/main/settings/')
    
    if target_user in current_user.followings.all():
        follow_text='CANCEL'
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
            value = Value.objects.get(user=user, date=datetime.now())
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

def createValue(user, target_date=None):
    last_value=Value.objects.filter(user=user, is_dummy=False).order_by('-date').first()
    # 최초 회원가입 시 value가 자동 생성되므로 last_value값이 없는 경우는 없음
    if target_date == None:
        target_date = timezone.now().date()
    
    percentage=0
    start = end = low = high = last_value.end
    value = Value.objects.create(
        user=user,
        date=target_date,
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
        text="CANCEL"
    elif buttonText == "CANCEL":
        current_user.followings.remove(target_user)
        text="FOLLOW"

    return JsonResponse({"text": text})

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
    
    followings_len = current_user.followings.count()
    
    context = {
        'user': current_user,
        'todos_levels_dict': todos_levels_dict,
        'followings': followings_len,
        'date_id':date_id, 
        'todos':todos,
        'todos_sub_dict': todos_sub_dict,
        'percent': value.percentage,
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

@csrf_exempt
def click_date(request, pk):
    #자바스크립트에서 날짜를 전달한다
    #views.py에서 그 날짜를 받고 날짜에 해당하는 value가 존재하는지 확인한다.
    #존재하면 -> value에 해당하는 todos를 보낸다
    #존재하지 않으면 -> todos == ''
    date_str = request.POST.get('date') #'8/21/2023'
    month_date_year = date_str.split('/')
    
    current_user = request.user
    #date_str을 date 자료형으로 변환
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    
    todos = []
    try:
        value = Value.objects.get(user=current_user,date=date_object)
        todo_objects = Todo.objects.filter(value=value)
        
        for todo in todo_objects:
            todo_data={
                'date_id':todo.value.pk,
                'content':todo.content,
                'goal_check':todo.goal_check,
                'id':todo.pk,
                'level':todo.level,
                'month':month_date_year[0],
                'date':month_date_year[1],
                'year':month_date_year[2],
            }
            todos.append(todo_data)
            
    except Value.DoesNotExist:
        todos = []

    return JsonResponse({'todos':todos})

#8월 1일 접속, 8월 3일 접속 -> 8월 3일의 value가 8월 1일 value를 기반으로 만들어져
#8월 1일 체크하면 -> 8월 3일 값의 변동은 다 반영이 됨
#8월 2일을 add_todo하고 check_todo -> 8월 2일도 8월 1일의 값을 기반으로 만들어졌기 때문에 8월 3일과 초깃값이 같고, 충돌
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

@csrf_exempt
def click_date(request):
    #자바스크립트에서 날짜를 전달한다
    #views.py에서 그 날짜를 받고 날짜에 해당하는 value가 존재하는지 확인한다.
    #존재하면 -> value에 해당하는 todos를 보낸다
    #존재하지 않으면 -> todos == ''
    date_str = request.POST.get('str') #'8/21/2023'
    month_date_year = date_str.split('/')

    username = request.POST.get("username")
    
    if username == "":
        target_user = request.user
    else:
        target_user = User.objects.get(username=username)
    
    #date_str을 date 자료형으로 변환
    date_object = datetime.strptime(date_str, '%m/%d/%Y').date()
    
    todos = []
    try:
        value = Value.objects.get(date=date_object, user=target_user)
        todo_objects = Todo.objects.filter(value=value)
        
        for todo in todo_objects:
            todo_data={
                'date_id':todo.value.pk,
                'content':todo.content,
                'goal_check':todo.goal_check,
                'id':todo.pk,
                'level':todo.level,
                'month':month_date_year[0],
                'date':month_date_year[1],
                'year':month_date_year[2],
            }
            todos.append(todo_data)
            
    except Value.DoesNotExist:
        todos = []

    return JsonResponse({'todos':todos})
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
        date_str = req['date_id']
        target_date = datetime.strptime(date_str, '%m/%d/%Y').date()
        
        #현재 user 객체 가져오기
        current_user = request.user
        #date 일치하는 value 객체 가져오기
        value = get_value_for_date(current_user, target_date)
        
        #value 없는 날-달력 연결 후 '완료'버튼 누르면 객체 생성
        if value == None:
            createValue(current_user, target_date)
            value = get_value_for_date(current_user, target_date)
        #value 있긴 한데 더미데이터 인 날
        if value.is_dummy:
            value.is_dummy = False
            last_value = Value.objects.filter(user=current_user, is_dummy=False, date__lt=target_date).order_by('-date').first()
            if last_value:
                value.start = value.end = value.low = value.high = last_value.end
            else:
                #만약 회원가입 일주일 전 ~ 회원가입날을 클릭한다면
                value.start = 0
                value.low = value.high = value.end = 50000

            value.save()
        
        #현재 user의 caregory 객체 가져오기
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
        
        todo = Todo.objects.get(pk=todo_id)
        value = todo.value
        
        #todo 삭제하기 전 연결된 value의 high값 업데이트
        value.high -= 1000*todo.level
        #todo 삭제하기 전 연결된 value의 low값 업데이트
        value.low += 1000*todo.level
        
        #저장
        value.save()
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
                value.percentage = round((value.end - 50000)/50000 * 100, 2)
            else:
                value.percentage = round((value.end - value.start)/value.start *100, 2) 
                
            todo.save()
            value.save()
            
        #combo변화 처리
        process_combo(current_user)
        todo_status = str(todo_status)
        return JsonResponse({'todo_status': todo_status, 't_id':todo.pk, 'percent':value.percentage})
        


"""
차트로 보낼 data준비하는 함수
"""
#유저의 최초회원가입 날짜로부터 경과한 날짜 반환하는 함수
# def days_since_joined(user):
#     delta = timezone.now() - user.date_joined
    
#     return delta.days   #int자료형으로 반환

def date_to_timestamp(date_obj):
    # return int(datetime.combine(date_obj, datetime.min.time()).timestamp() * 1000) + timedelta(days=1)
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
                is_dummy=True,
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
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.now(kst).date()

    values = Value.objects.filter(user=user, date__lte=today).order_by('-date')

    
    #역순으로 체크
    combo = 0
    previous_date = None

    for value in values:
        todos = Todo.objects.filter(value=value)
        success_day = any(todo.goal_check for todo in todos)
    
        #previous_date가 설정되어 있고 그 간격이 1 이상이거나 체크한 날이 아니면 반복문 탈출
        if (previous_date and previous_date - value.date > timedelta(days=1)) or not success_day:
            print('탈출')
            break
        print('previous_date:', previous_date)
        print('valid_date:', value.date)
        
        combo += 1
        print('combo 증가:', combo)
        previous_date = value.date
        
    user.combo = combo
    user.save()
        
    return

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
    return render(request, 'main/category.html')


# group
def group(request,pk):
    group = Group.objects.get(id=pk)
    users = group.user_set.all()  # 그룹에 연결된 사용자들을 가져옵니다.
    value_dic={}
    my_group = request.user.my_group

    if group.create_user == request.user.name:
        am_I_creator = True
    else:
        am_I_creator = False

    if my_group == group.name:
        button_text = "CANCEL"
    else:
        button_text = "FOLLOW"    
    # value_dic에 사용자 이름과 해당 사용자의 value를 넣어줍니다.
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
    }
    return render(request, 'main/group.html', context)



@csrf_exempt
def follow_group(request):
    buttonText = request.POST.get("buttonText")
    group = request.POST.get("group")
    target_group = Group.objects.get(name=group)
    current_user = request.user

    if buttonText == "FOLLOW":
        current_user.my_group = target_group
        text="CANCEL"
    elif buttonText == "CANCEL":
        current_user.my_group = None
        text="FOLLOW"

    current_user.save()

    return JsonResponse({"text": text})

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

            redirect(f'/main/group/{user.my_group.id}')
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
        
        return redirect('/main/settings/')
    