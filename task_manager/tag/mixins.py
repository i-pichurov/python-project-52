from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginRequiredMessageMixin(LoginRequiredMixin):
    """Добавляет сообщение при редиректе неавторизованного пользователя."""

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect(settings.LOGIN_URL)
