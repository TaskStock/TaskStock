from django.shortcuts import render
from .models import *
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

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
        
        Todo.objects.create(
            content=content,
            level=level,
            goal_check=False
        )
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
        
        todo = Todo.objects.get(id=todo_id)
        if todo_status == 'checked':
            #가치 상승 계산
            pass
        else:
            #가치 하락 계산
            pass
        

#---지수 작업---#

#---선우 작업---#