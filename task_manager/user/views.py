from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages


# Create your views here.
def index(request):
    return HttpResponse("user")


class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html' # путь к шаблону
    context_object_name = 'users' # переменная в шаблоне
    paginate_by = 20 # пагинация по 20 пользователей


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно изменен'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('users_list')
        
        if int(self.kwargs['pk']) != request.user.pk:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users_list')
    
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Редактируем текущего пользователя
        return self.request.user
        #return User.objects.get(pk=2)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users_list')
    success_message = 'Пользователь успешно удален'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect('users_list')
        
        if int(self.kwargs['pk']) != request.user.pk:
            messages.error(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect('users_list')
        
        return super().dispatch(request, *args, **kwargs)

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