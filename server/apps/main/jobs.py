from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from server.apps.task_account.models import *
from .views import *
import datetime



scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")
#하루에 한번 - 우리나라만 대상으로 할 경우 UTC기준 15시에 한번씩 실행되게 하면 됨
#@register_job(scheduler, "interval", days=1, next_run_time=datetime.datetime.now().replace(hour=15, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1))

#글로벌 대응 - 매 시 정각마다 실행
#@register_job(scheduler, "interval", hours=1, next_run_time=datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1))

#테스트용 - 1분에 한번씩
@register_job(scheduler, "interval", minutes=1, next_run_time=datetime.datetime.now() + datetime.timedelta(minutes=1), replace_existing=True)
def porcess_decrease():
    users = User.objects.all()
    
    for user in users:
        current_time = get_current_arrow(user.tzinfo)   #사용자의 로컬 시간대
        
        #원래 로직
        #if current_time.hour == 0 and current_time.minute == 0:
            #previous_day = current_time.shift(days=-1)
        
        #테스트용
        previous_day = current_time
        decrease_value(user, previous_day)
    
    return

if not scheduler.running:
    register_events(scheduler)
    scheduler.start()
    print("Scheduler 실행")




