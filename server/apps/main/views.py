from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Create your views here.
#---정근 작업---#

#---환희 작업---#
def hello():
    pass
#---세원 작업---#
"""
할 일 추가 버튼 누름 -> 새로운 Todo객체 생성
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
        date = datetime.now().strftime('%Y-%m-%d')
        date_time = date + '06:00:00'
        
        value = Value.objects.get(date=date_time)
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
할일 완료에 체크 표시 -> 가치 상승 계산 -> value에 create
"""
def complete_task(request):
    if request.method == "POST":
        req = json.loads(request.body)
        todo_id = req['id']
        todo_status = req['status']
        
        #해당되는 Todo 객체 가져오기
        todo = Todo.objects.get(id=todo_id)
        
        #사용자와 관련된 value 객체 가져오기
        user_value = Value.objects.get(user=request.user)
        
        #가치 계산
        if todo_status == 'checked':
            #가치 상승 계산
            pass
        else:
            #가치 하락 계산
            pass
        

#---지수 작업---#

#---선우 작업---#