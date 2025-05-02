from django.urls import path
from task_manager.user.views import (
    UserIndexView,
    UserCreateView,
)

urlpatterns = [
    path("", UserIndexView.as_view(), name='users_list'),
    path("create/", UserCreateView.as_view(), name='users_create')
]