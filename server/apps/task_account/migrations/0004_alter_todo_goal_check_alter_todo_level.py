# Generated by Django 4.2.4 on 2023-08-04 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_account', '0003_alter_todo_goal_check_alter_todo_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='goal_check',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='todo',
            name='level',
            field=models.IntegerField(),
        ),
    ]