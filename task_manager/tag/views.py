from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db.models import ProtectedError
from .models import Tag
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
class TagIndexView(LoginRequiredMessageMixin, ListView):
    model = Tag
    template_name = 'tags/index.html' # путь к шаблону
    context_object_name = 'tags' # переменная в шаблоне


class TagCreateView(LoginRequiredMessageMixin, SuccessMessageMixin, CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tags/create.html'
    success_url = reverse_lazy('tags_list')
    success_message = 'Метка успешно создана'


class TagUpdateView(LoginRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = Tag
    fields = ['name']
    template_name = 'tags/update.html'
    success_url = reverse_lazy('tags_list')
    success_message = 'Метка успешно изменена'


class TagDeleteView(LoginRequiredMessageMixin, DeleteView):
    model = Tag
    template_name = 'tags/tag_confirm_delete.html'
    success_url = reverse_lazy('tags_list')
    success_message = 'Метка успешно удалена'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, 'Невозможно удалить тег, так как он используется в задачах.')
            return redirect(self.success_url)
