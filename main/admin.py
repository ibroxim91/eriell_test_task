from typing import Any
from django import forms
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from .models import User, Group, Score, Science, LessonPlan, GroupStudents
from .positions import student, teacher, director


# Чтобы избежать дублирования кода
class GetQuerySet:
       
    # Чтобы преподаватель  видел только свои записи 
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        user = request.user
        position = getattr(user, 'position', None)
        if position == teacher:
            return super().get_queryset(request).filter(teacher=user)  
        if position == student:
            return Group.objects.filter(group_students__student=user)  
        return super().get_queryset(request)
    

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "get_full_name", "position")


@admin.register(Group)
class GroupAdmin(GetQuerySet, admin.ModelAdmin):
    list_display = ("id", "teacher", "name")

    def get_form(self, request, obj, **kwargs):
        form = super(GroupAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['teacher'] = forms.ModelChoiceField(User.objects.filter(position=teacher))
        return form  
    

@admin.register(LessonPlan)
class LessonPlanAdmin(GetQuerySet, admin.ModelAdmin):
    list_display = ("teacher", "name")

    def get_form(self, request, obj, **kwargs):
        form = super(LessonPlanAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['teacher'] = forms.ModelChoiceField(User.objects.filter(position=teacher))
        return form  


@admin.register(Science)
class ScienceAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("id", "science", "group", "student", "point")

    # преподаватель может выбирать только своих учеников и group
    def get_form(self, request, obj, **kwargs):

        form = super(ScoreAdmin, self).get_form(request, obj, **kwargs)
        if request.user.position == teacher:
            form.base_fields['student'] = forms.ModelChoiceField(queryset=request.user.teacher_students())
            form.base_fields['group'] = forms.ModelChoiceField(queryset=Group.objects.filter(teacher=request.user))
        if request.user.position == director:
            form.base_fields['student'] = forms.ModelChoiceField(User.objects.filter(position=student))
        return form  

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        user = request.user
        position = getattr(user, 'position', None)
        if position == teacher:
            return super().get_queryset(request).filter(teacher=user)  
        if position == student:
            return super().get_queryset(request).filter(student=user)  
        return super().get_queryset(request)
   
    
@admin.register(GroupStudents)
class GroupStudentsAdmin(GetQuerySet, admin.ModelAdmin):
    list_display = ("group", "student", "status")

    def get_form(self, request, obj, **kwargs):

        form = super(GroupStudentsAdmin, self).get_form(request, obj, **kwargs)
        if request.user.position == teacher:
            form.base_fields['student'] = forms.ModelChoiceField(queryset=request.user.teacher_students())
        if request.user.position == director:
            form.base_fields['student'] = forms.ModelChoiceField(User.objects.filter(position=student))
        return form  
   