from django.shortcuts import render
from django.views import View
from .mypermission import PermissionView
from .models import User, Group, Science, Score
# Create your views here.


class HomeView(PermissionView, View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, "index.html", {"users": users})


class GroupView(PermissionView, View):

    def get(self, request, *args, **kwargs):
        groups = Group.objects.all()
        return render(request, "groups.html", {"groups": groups})    


class ScienceView(PermissionView, View):

    def get(self, request, *args, **kwargs):
        science = Science.objects.all()
        return render(request, "science.html", {"science": science})      


class ScoreView(PermissionView, View):

    def get(self, request, *args, **kwargs):
        score = Score.objects.all()
        return render(request, "score.html", {"score": score})
