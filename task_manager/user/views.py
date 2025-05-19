from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from .mixins import CustomUserLoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.db.models import ProtectedError
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html' # путь к шаблону
    context_object_name = 'users' # переменная в шаблоне


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(CustomUserLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно изменен'

    def get_object(self, queryset=None):
        # Редактируем текущего пользователя
        return self.request.user


class UserDeleteView(CustomUserLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удален'

    def get_object(self, queryset=None):
        return self.request.user


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        # Добавляем сообщение об успешной авторизации
        messages.success(self.request, 'Вы успешно вошли в систему!')
        # Важно вызвать родительский метод form_valid для завершения процесса входа
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы успешно вышли из системы.")
        return super().dispatch(request, *args, **kwargs)