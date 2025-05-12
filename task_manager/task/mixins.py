from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task


class LoginRequiredMessageMixin(LoginRequiredMixin):
    """Добавляет сообщение при редиректе неавторизованного пользователя."""

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect(settings.LOGIN_URL)


class CustomUserLoginRequiredMixin:
    """Только авторизованный пользователь и только к собственной задаче."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(settings.LOGIN_URL)

        task = get_object_or_404(Task, pk=kwargs.get('pk'))
        if task.creator != request.user:
            messages.error(request, 'Задачу может удалить только ее автор')
            return redirect('tasks_list')

        return super().dispatch(request, *args, **kwargs)
