from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import pytz
from datetime import timedelta, datetime, time


# 비밀번호 변경 위한 라이브러리
from django.contrib.auth.hashers import check_password
from django.contrib import auth

from django.core.exceptions import ObjectDoesNotExist

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

def createValue(user):
    last_value=Value.objects.filter(user=user).order_by('-date').first()
    # 마지막 생성된 value 기준으로 새로운 value 값들을 계산하는 로직 필요
    # 최초 회원가입 시 value가 자동 생성되므로 last_value값이 없는 경우는 없음
    percentage=0
    start_datetime=50000
    end=0
    low=0
    high=0
    combo=0
    value = Value.objects.create(
        user=user,
        date=timezone.now(),
        percentage=percentage,
        start_datetime=start_datetime,
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
    
    #데이터
    dataset = values_for_chart(current_user, 5)
    return render(request, 'main/home.html', {'date_id':date_id, 'todos':todos, 'dataset':dataset})

def hello(request):
    context = {
                
            }
    return render(request, 'base.html', context=context)

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
    # start_datetime_date는 오늘 날짜의 자정(DB에 UTC 기준으로 저장되어 있으니까 UTC로 변환)
    start_datetime_date = today_date.astimezone(pytz.UTC)
    print(start_datetime_date)
    # end_date는 start_datetime_date에서 1일 후 (UTC로 변환)
    end_date = start_datetime_date + timezone.timedelta(days=1)
    print(end_date)
    # date__gte와 date__lt를 사용하여 해당 범위 내의 Value 객체 가져오기
    value_object = Value.objects.get(user=user, date__gte=start_datetime_date, date__lt=end_date)
        
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
            value.end += 1000*todo.level
        else:
            todo.goal_check = False
            value.end -= 1000*todo.level
        
        #value의 percentage값 업데이트
        value.percentage = int((value.end-value.start_datetime)/value.start_datetime *100)
        if value.percentage > 0:
            color = 'blue'
        else:
            color = 'red'
            
        todo.save()
        value.save()
        
        return JsonResponse({'color':color, 'value':value, 'todo':todo})

#유저의 최초회원가입 날짜로부터 경과한 날짜 반환하는 함수
def days_since_joined(user):
    delta = timezone.now() - user.date_joined
    return delta.days   #int자료형으로 반환


"""
차트로 보낼 data준비하는 함수
"""
def values_for_chart(user, term):
    kst = pytz.timezone('Asia/Seoul')
    max_date = days_since_joined(user)  #int
    #db에 UTC기준으로 저장되어있으니까 now()사용
    utc_datetime = timezone.now()
    print('utc_datetime:', utc_datetime)

    #회원가입 후 지난 기간 == 유저의 최대 value 개수
    #유저의 최대 value개수가 프론트에서 요청한 term보다 적을 경우 그냥 최대 value개수 만큼만 보냄
    if max_date < term:
        start_datetime =  utc_datetime - timedelta(days=term)#원래는 days=max_date
        print('start_datetime', start_datetime)
    #그렇지 않을 경우 요청한 term만큼의 value데이터 보냄(비어있는 date의 value는 만들어서)
    else:
        start_datetime = utc_datetime - timedelta(days=term)
        print('start_datetime', start_datetime)
    
    #사용자가 요청한 범위의 date
    all_dates = {start_datetime.date() + timedelta(days=i) for i in range(1, term+1)}
    print('사용자가 요청한 datetime:', all_dates)
    
    #이미 db에 존재하는 date들
    #value객체 필터링
    range_values = Value.objects.filter(user=user, date__range=(start_datetime, utc_datetime))
    #value객체에서 datetime만 뽑아오기
    value_dates = set(d.date() for d in range_values.values_list('date', flat=True))
    print('db에 있는 datetime:', value_dates)
    
    #없는 날짜 처리
    missing_dates = list(all_dates - value_dates) #set으로 차집합 구하고 list로 변환
    missing_dates.sort() #날짜순으로 정렬
    print('없는 datetime:', missing_dates)
    
    #없는 날짜가 있는경우
    if missing_dates:
        for missing_date in missing_dates:
            previous_date_start = datetime.combine(missing_date - timedelta(days=1), datetime.min.time())
            previous_date_end = datetime.combine(missing_date - timedelta(days=1), datetime.max.time())

            # 이 범위를 사용하여 Value 객체를 필터링합니다.
            latest_value = Value.objects.filter(user=user, date__range=(previous_date_start, previous_date_end)).first()
            #missing_date의 UST기준 날짜 넣는데 이건 또 kst로 들어가서 ust로 바꿔줌
            Value.objects.create(
                user=user,
                date=missing_date + timedelta(days=1),
                percentage=0,
                start=latest_value.end,
                end=latest_value.end,
                low=latest_value.end - 1000,
                high=latest_value.end,
                combo=latest_value.combo,
            )

    #새로 만든 value들 포함해서 가져오기
    values = Value.objects.filter(user=user, date__range=(start_datetime, utc_datetime))
    print(values)
    values = list(values)
    
    dataset = [[int((value.date.replace(hour=0, minute=0, second=0, microsecond=0)+timedelta(days=1)).timestamp()*1000), value.start, value.high, value.low, value.end] for value in values]
        
    return dataset

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