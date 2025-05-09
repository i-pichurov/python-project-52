from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings


class CustomUserLoginRequiredMixin:
    """Только авторизованный пользователь и только к собственному объекту."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(settings.LOGIN_URL)

        if 'pk' in kwargs and int(kwargs['pk']) != request.user.pk:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users_list')

        return super().dispatch(request, *args, **kwargs)