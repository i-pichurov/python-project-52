from django.urls import path
from task_manager.task.views import (
    TaskIndexView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView
)

urlpatterns = [
    path("", TaskIndexView.as_view(), name='tasks_list'),
    path("create/", TaskCreateView.as_view(), name='tasks_create'),
    path("<int:pk>/", TaskDetailView.as_view(), name='tasks_detail'),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name='tasks_update'),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name='tasks_delete'),
]