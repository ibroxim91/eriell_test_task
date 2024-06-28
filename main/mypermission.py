from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.shortcuts import render 
from .positions import director


class PermissionView(PermissionRequiredMixin):
    login_url = "/login/"
    permission_denied_message = "Для входа в систему сначала введите пароль для входа"
    permission_required = 'main.view_group'
    def handle_no_permission(self):
        user = self.request.user
        if not user.is_authenticated:
            messages.add_message(self.request, messages.WARNING, "Для входа в систему сначала введите пароль для входа")
            return render(self.request, "login.html")
        if user.position == director:
            return True
        else:
            messages.add_message(self.request, messages.WARNING, "У вас нет разрешения на доступ к запрошенной странице")
            return render(self.request, "login.html")
                