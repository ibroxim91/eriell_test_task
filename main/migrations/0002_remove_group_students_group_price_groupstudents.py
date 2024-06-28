# Generated by Django 4.2 on 2024-06-26 04:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='students',
        ),
        migrations.AddField(
            model_name='group',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Payment amount'),
        ),
        migrations.CreateModel(
            name='GroupStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('lid', 'lid'), ('active', 'active'), ('trial', 'trial'), ('paused', 'paused'), ('arxived', 'arxived'), ('left', 'left'), ('completed', 'completed')], max_length=20, verbose_name='Status')),
                ('add_date', models.DateTimeField(auto_now_add=True, verbose_name='Add date')),
                ('left_date', models.DateTimeField(blank=True, null=True, verbose_name='Left date')),
                ('pay_summa', models.IntegerField(default=0, verbose_name='Individual payment amount')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_students', to='main.group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
