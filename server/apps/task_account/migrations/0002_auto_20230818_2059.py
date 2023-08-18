from django.db import migrations

def add_initial_badges(apps, schema_editor):
    Badge = apps.get_model('task_account', 'Badge')
    
    badge_data = [
        ('지금이라도 사야해', 'combo 10일 달성'),
        ('개미의 선택', '가치 10만원 돌파'),
        ('슈퍼 개미의 선택', '가치 20만원 돌파'),
        ('우주 개미의 선택', '가치 50만원 돌파'),
        ('콩콩', '주가 22% 상승'),
        ('1+1', '주가 100% 상승'),
        ('화성 갈끄니까', '가치 100만원 돌파')
    ]

    for name, description in badge_data:
        Badge.objects.create(name=name, description=description)


class Migration(migrations.Migration):
		#여기는 알아서 만들어줌, 이전 마이그레이션 파일에 따라 유도리 있게
    dependencies = [
        ('task_account', '0001_initial'),
    ]
		
    operations = [
        migrations.RunPython(add_initial_badges),
    ]