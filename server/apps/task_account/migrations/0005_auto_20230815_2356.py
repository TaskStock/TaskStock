from django.db import migrations

def add_initial_badges(apps, schema_editor):
    Badge = apps.get_model('task_account', 'Badge')
    
    badge_names = ['화성 갈끄니까']
    for name in badge_names:
        Badge.objects.create(name=name)
    

class Migration(migrations.Migration):

    dependencies = [
        ('task_account', '0004_auto_20230815_2348'),
    ]

    operations = [
        migrations.RunPython(add_initial_badges),
    ]


