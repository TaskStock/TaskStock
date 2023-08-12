# Generated by Django 4.2.4 on 2023-08-12 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_account', '0005_category_finish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='todo_category', to='task_account.category'),
        ),
    ]
