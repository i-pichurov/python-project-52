from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Task
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import LoginRequiredMessageMixin, CustomUserLoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)


# Create your views here.
class TaskIndexView(LoginRequiredMessageMixin, ListView):
    model = Task
    template_name = 'tasks/index.html' # путь к шаблону
    context_object_name = 'tasks' # переменная в шаблоне
    paginate_by = 20 # пагинация по 20 пользователей


class TaskCreateView(LoginRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'status', 'performer']
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.creator = self.request.user  # автоматически подставляем текущего пользователя
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'performer']
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно изменена'


class StatusDeleteView(CustomUserLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно удалена'
