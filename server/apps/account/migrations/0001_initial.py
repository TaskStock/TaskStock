# Generated by Django 4.2.4 on 2023-08-02 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Todolist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmp', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_created=True, auto_now_add=True)),
                ('percentage', models.FloatField()),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('low', models.IntegerField()),
                ('high', models.IntegerField()),
                ('combo', models.IntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('content', models.TextField()),
                ('goal_check', models.BooleanField()),
                ('level', models.IntegerField()),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('finish_time', models.DateTimeField(null=True)),
                ('todolist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_todolist', to='account.todolist')),
                ('value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todo_value', to='account.value')),
            ],
        ),
    ]
