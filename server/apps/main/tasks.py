# from celery import shared_task
# from task_account.models import *
# from .views import *

# def is_local_midnight(user):
#     if 
    


# @shared_task
# def decrease_value():
#     # 유저에 대한 작업 수행
#     #투두 체크 및 가치 감소 로직 수행
#     # user_id를 기반으로 해당 유저의 투두 정보를 가져와 처리
#     current_time = arrow.utcnow()
#     users = .objects.filter(date__hour=0, date__minute=0) ㅇ
    
#     start_
#     for user in users:
#         value = Value.objects.filter(user=user, date__gte=).first()
#         todos = Todo.objects.get(value=value)
#         value.assigned = True
#         for todo in todos:
#             if not todo.goal_check:
#                 value.end -= 1000*todo.level



# def process_combo(user):
#     # 사용자의 시간대를 기반으로 현재 arrow을 가져옴
#     current_local_arrow = get_current_arrow(user.tzinfo)
#     # UTC로 변환
#     current_utc_arrow = local_to_utc(current_local_arrow)
    
#     # 오늘 UTC datetime 기준으로 조회
#     values = Value.objects.filter(user=user, date__lte=current_utc_arrow.datetime).order_by('-date')

#     # 역순으로 체크
#     combo = 0
#     previous_datetime = None

#     for value in values:
#         todos = Todo.objects.filter(value=value)
#         success_day = any(todo.goal_check for todo in todos)
    
#         # previous_datetime이 설정되어 있고 그 간격이 1 일 이상이거나 체크한 날이 아니면 반복문 탈출
#         if previous_datetime and (previous_datetime - value.date > timedelta(days=1)) or not success_day:
#             break
        
#         combo += 1
#         previous_datetime = value.date
        
#     user.combo = combo
#     user.save()
        
#     return
