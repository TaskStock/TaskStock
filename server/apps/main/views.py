from django.shortcuts import render, redirect
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
"""
사용자가 로그인 할 때마다 value객체 검증하고 사용자의 가치 update
할일 추가 함수
할일 삭제 함수
체크 상태에 따라 가치 계산하는 함수
난이도 변경에 따라 가치 계산하는
할일 수정 함수
팔로잉 검색하는 함수
팔로우 검색하는 함수
전체 사람 중에 검색하는 함수
"""

# Create your views here.
# ---정근 작업---#

# ---환희 작업---#

def home(request):
    return render(request, 'base.html')

#---세원 작업---#

"""
오늘 06:00:00이랑 다음날 06:00:00까지의 value객체 가져오는 함수
"""
def get_todayValue():
    today = datetime.now().strftime('%Y-%m-%d')
    start_date = today + ' 06:00:00' #이상
    end_date = today[:-1] + str(int(today[-1]) + 1) + ' 06:00:00' #미만
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
        todos = Todo.objects.filter(value=value)
        todo = todos[-1]
        todo_id = todo.pk
        
        #todo의 high값 업데이트
        todos_cnt = todos.count()
        todo.value.low += todo.level*1000
        
        #todo의 low값 업데이트
        todo.value.high -= 1000
        
        #방금 만들어진 todo 가져오기/수정하거나 삭제해야할 것 같아서 걍 id로 보냄
        todo.save()
        return JsonResponse({'content':content, 'level':level, 'todo_id':todo_id})

"""
Todo 삭제 하는 함수
할 일 삭제 버튼 누름 -> todo 객체 삭제(ajax)
"""
@csrf_exempt
def delete_todo(request, pk):
    if request.method == 'POST':
        req =  json.loads(request.body)
        todo_id = req['id']
        
        todo_object = Todo.objects.get(pk=todo_id)
        todo_object.delete()
        
    return JsonResponse({'todo_id':todo_id})


"""
할일 완료에 체크 표시/해제 -> 가치 등락 계산 -> end, percentage update
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
            todo.value.end = todo.value.start + 1000*todo.level
        else:
            todo.goal_check = False
            todo.value.end = todo.value.start - 1000*todo.level
        
        todo.value.percentage = int((todo.value.end-todo.value.start)/todo.value.start *100)
        if todo.value.percentage < 0:
            color = 'blue'
            todo.value.percentage = abs(todo.value.percentage)
        else:
            color = 'red'
            
        todo.save()
        return JsonResponse({'color':color})

def search(request):
    return render(request, 'main/search.html')

#---선우 작업---#