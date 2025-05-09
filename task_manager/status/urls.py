from django.urls import path
from task_manager.status.views import (
    StatusIndexView,
    StatusCreateView,
    StatusUpdateView,
    StatusDeleteView,
)

urlpatterns = [
    path("", StatusIndexView.as_view(), name='statuses_list'),
    path("create/", StatusCreateView.as_view(), name='statuses_create'),
    path("<int:pk>/update/", StatusUpdateView.as_view(), name='statuses_update'),
    path("<int:pk>/delete/", StatusDeleteView.as_view(), name='statuses_delete'),
]