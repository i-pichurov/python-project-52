from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from django.db.models import ProtectedError
from django.urls import reverse_lazy


class CustomUserLoginRequiredMixin:
    """Только авторизованный пользователь и только к собственному объекту."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(settings.LOGIN_URL)

        if 'pk' in kwargs and int(kwargs['pk']) != request.user.pk:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users_list')

        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить пользователя, так как он используется в задачах.')
            return redirect(reverse_lazy('users_list'))