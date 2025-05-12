from django.urls import path
from task_manager.task.views import (
    TaskIndexView,
    TaskCreateView,
    StatusUpdateView,
    StatusDeleteView
)

urlpatterns = [
    path("", TaskIndexView.as_view(), name='tasks_list'),
    path("create/", TaskCreateView.as_view(), name='tasks_create'),
    path("<int:pk>/update/", StatusUpdateView.as_view(), name='tasks_update'),
    path("<int:pk>/delete/", StatusDeleteView.as_view(), name='tasks_delete'),
]