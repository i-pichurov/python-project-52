from django.urls import path
from task_manager.status.views import (
    StatusIndexView,
    StatusCreateView,
)

urlpatterns = [
    path("", StatusIndexView.as_view(), name='statuses_list'),
    path("create/", StatusCreateView.as_view(), name='statuses_create'),
]