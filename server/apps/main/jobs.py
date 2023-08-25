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
    users = User.objects.all()
    current_time = get_current_arrow('Asia/Seoul')   
    previous_day = current_time.shift(days=-1)
    
    for user in users:
        try:
            decrease_value(user, previous_day)
        except Exception as e:
            print(f"Error decreasing value for user {user.id}: {e}")
            continue

        try:
            alarm_calculate_account(user, previous_day)
        except Exception as e:
            print(f"Error in alarm_calculate_account for user {user.id}: {e}")
            continue

        try:
            alarm_calculate_follow(user)
        except Exception as e:
            print(f"Error in alarm_calculate_follow for user {user.id}: {e}")
            continue

    # 그룹과 랭킹 알람은 유저 각각이 실행하면 안됨
    try:
        alarm_calculate_group()
    except Exception as e:
        print(f"Error in alarm_calculate_group: {e}")

    try:
        alarm_calculate_ranking()
    except Exception as e:
        print(f"Error in alarm_calculate_ranking: {e}")


    # 하루 동안의 결과를 알람으로 보낸 후 업데이트 해야함
    with transaction.atomic():
        groups = Group.objects.select_for_update().all()
        for group in groups:
            group.delta = 0
            group.save()

    with transaction.atomic():
        per_users=User.objects.select_for_update().all()
        for user in per_users:
            user.percentage = 0
            user.save()


if not scheduler.running:
    register_events(scheduler)
    scheduler.start()
    print("Scheduler 실행")

