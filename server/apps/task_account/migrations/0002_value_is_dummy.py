# Generated by Django 4.2.4 on 2023-08-10 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='is_dummy',
            field=models.BooleanField(default=False),
        ),
    ]
