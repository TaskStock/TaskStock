from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Create your views here.
# ---정근 작업---#

# ---환희 작업---#

def home(request):
    return render(request, 'main/home.html')

def hello(request):
    context = {
                
            }
    return render(request, 'base.html', context=context)
  
#---세원 작업---#
"""
날마다 유저마다 하나씩 value 객체를 생성해줌
"""
def set_personal_value():
    pass
"""
오늘 06:00:00이랑 다음날 06:00:00까지의 value객체 가져오는 함수
"""
def get_todayValue():
    today = datetime.now().strftime('%Y-%m-%d')
    start_date = today + ' 06:00:00'
    end_date = today[:-1] + str(int(today[-1]) + 1) + ' 06:00:00'
    value_object = Value.objects.get(date__gte=start_date, date__lt=end_date)

    return value_object


"""
할 일 추가 버튼 누름 -> 새로운 Todo객체 생성(ajax로 구현할 예정)
"""
@csrf_exempt
def add_todo(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        content = req['content']
        level = req['level']
        #현재 user 객체 가져오기
        current_user = request.user
        
        #date 일치하는 value 객체 가져오기 YYYY-MM-DD HH:MM:SS
        value = get_todayValue()
        
        #현재 user의 todolist 객체 가져오기
        todolist = Todolist.objects.get(user=current_user)
        
        #투두 객체 생성
        Todo.objects.create(
            value = value,
            todolist=todolist,
            content=content,
            level=level,
            goal_check=False
        )
        
        #방금 만들어진 todo 가져오기/수정하거나 삭제해야할 것 같아서 걍 id로 보냄
        todo_id = Todo.objects.last().pk
        
        return JsonResponse({'content':content, 'level':level, 'todo_id':todo_id})

"""
할일 완료에 체크 표시/해제 -> 가치 등락 계산 -> value update
"""
def check_task(request):
    if request.method == "POST":
        req = json.loads(request.body)
        todo_id = req['id']
        todo_status = req['status']
        
        #해당되는 Todo 객체 가져오기
        todo = Todo.objects.get(id=todo_id)
        #오늘의 value 가져오기
        value = get_todayValue()
        
        #status에 따라 goal_check 변경
        if todo_status == 'checked':
            todo.goal_check = True
        else:
            todo.goal_check = False

        todos_cnt = Todo.objects.filter(value__in=value).count()
        todos = Todo.objects.filter(value=value)
        delta = 0
        for todo in todos:
            delta += todo.level
    
        #가치 상승
        if todo.goal_check:
            pass


def search(request):
    return render(request, 'main/search.html')

#---선우 작업---#