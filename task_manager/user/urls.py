from django.urls import path
from task_manager.user.views import (
    UserIndexView,
    UserCreateView,
    UserUpdateView,
    UserDeleteView,
)

urlpatterns = [
    path("", UserIndexView.as_view(), name='users_list'),
    path("create/", UserCreateView.as_view(), name='users_create'),
    path("<int:pk>/update/", UserUpdateView.as_view(), name='users_update'),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name='users_delete'),
]