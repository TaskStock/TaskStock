# Generated by Django 4.2.4 on 2023-08-15 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_account', '0005_auto_20230815_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='value',
            name='is_updated',
            field=models.BooleanField(default=False),
        ),
    ]
