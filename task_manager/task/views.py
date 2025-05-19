from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Task
from django.contrib.auth.models import User
from task_manager.status.models import Status
from task_manager.tag.models import Tag
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import LoginRequiredMessageMixin, CustomUserLoginRequiredMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)


# Create your views here.
class TaskIndexView(LoginRequiredMessageMixin, ListView):
    model = Task
    template_name = 'tasks/index.html' # путь к шаблону
    context_object_name = 'tasks' # переменная в шаблоне

    def get_queryset(self):
        queryset = Task.objects.select_related('status', 'performer', 'creator')

        status_id = self.request.GET.get('status')
        performer_id = self.request.GET.get('performer')
        only_my = self.request.GET.get('only_my')
        tag_id = self.request.GET.get('tags')

        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if performer_id:
            queryset = queryset.filter(performer_id=performer_id)
        if only_my:
            queryset = queryset.filter(creator=self.request.user)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_list'] = Status.objects.all()
        context['user_list'] = User.objects.all()
        context['tag_list'] = Tag.objects.all()
        context['request'] = self.request  # чтобы шаблон мог читать GET-параметры
        return context


class TaskCreateView(LoginRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'status', 'performer', 'tags']
    template_name = 'tasks/create.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно создана'

    def form_valid(self, form):
        form.instance.creator = self.request.user  # автоматически подставляем текущего пользователя
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'performer', 'tags']
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно изменена'


class TaskDeleteView(CustomUserLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = 'Задача успешно удалена'


class TaskDetailView(LoginRequiredMessageMixin, DetailView):
    model = Task
    template_name = 'tasks/detail.html'
    context_object_name = 'task'