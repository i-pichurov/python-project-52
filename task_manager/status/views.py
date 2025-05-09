from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Status
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import LoginRequiredMessageMixin
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)   


# Create your views here.
class StatusIndexView(LoginRequiredMessageMixin, ListView):
    model = Status
    template_name = 'statuses/index.html' # путь к шаблону
    context_object_name = 'statuses' # переменная в шаблоне
    paginate_by = 20 # пагинация по 20 статусов


class StatusCreateView(LoginRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = 'Статус успешно создан'


class StatusUpdateView(LoginRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/update.html'
    success_url = reverse_lazy('statuses_list')
    success_message = 'Статус успешно изменен'


class StatusDeleteView(LoginRequiredMessageMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = 'Статус успешно удален'
