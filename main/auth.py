from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")
    
    def post(self, request):
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 "Авторизация успешно завершена Добро пожаловать в программу")
            return redirect("/")
        else:
            messages.add_message(request, messages.WARNING,
                                 "При входе произошла ошибка. Пожалуйста, проверьте свой пароль еще раз.")
            return redirect("/login")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login')
