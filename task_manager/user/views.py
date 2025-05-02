from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.urls import reverse_lazy

# Create your views here.
def index(request):
    return HttpResponse("user")

class UserIndexView(ListView):
    model = User
    template_name = 'users/index.html' # путь к шаблону
    context_object_name = 'users' # переменная в шаблоне
    paginate_by = 20 # пагинация по 20 пользователей

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')

class UserCreateView(CreateView):
        form_class = CustomUserCreationForm
        template_name = 'users/create.html'
        success_url = reverse_lazy('users_list')
