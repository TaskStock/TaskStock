# Generated by Django 3.2 on 2023-08-17 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_account', '0002_auto_20230817_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='password',
        ),
        migrations.AddField(
            model_name='group',
            name='create_user_id',
            field=models.CharField(default='', max_length=30),
        ),
    ]