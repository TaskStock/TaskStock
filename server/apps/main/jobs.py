from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from server.apps.task_account.models import *
from .views import *
import arrow

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
#글로벌 대응 - 매 시 정각마다 실행
#next_run = arrow.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).shift(hours=1).datetime
#@register_job(scheduler, "interval", hours=1, next_run_time=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1))

#테스트용 - 5분에 한번씩
#next_run = arrow.utcnow().shift(minutes=5).datetime
#@register_job(scheduler, "interval", minutes=5, next_run_time=next_run, replace_existing=True)

# 하루에 한번 - 우리나라만 대상으로 할 경우 UTC기준 15시/KST기준 00시에 한번씩 실행되게 하면 됨
next_run = arrow.now('Asia/Seoul').replace(hour=0, minute=0, second=0, microsecond=0).shift(days=1).datetime
@register_job(scheduler, "interval", days=1, next_run_time=next_run, replace_existing=True)
def porcess_midnight():
    groups = Group.objects.all()
    for group in groups:
        group.delta = 0
        group.save()
    
    users = User.objects.all()
    for user in users:
        current_time = get_current_arrow(user.tzinfo)   #사용자의 로컬 시간대
        #if current_time.hour == 0 and current_time.minute == 0: #글로벌 대응용 로직
        
        previous_day = current_time.shift(days=-1)
        decrease_value(user, previous_day)

        #add_delta_to_group(user, previous_day)

        # 정산 결과 알림
        alarm_calculate_account(user, previous_day)
        alarm_calculate_follow(user)
        alarm_calculate_group()
        alarm_calculate_ranking()
    
    return


if not scheduler.running:
    register_events(scheduler)
    scheduler.start()
    print("Scheduler 실행")

