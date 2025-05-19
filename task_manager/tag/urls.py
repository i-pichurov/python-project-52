from django.urls import path
from task_manager.tag.views import (
    TagIndexView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
)

urlpatterns = [
    path("", TagIndexView.as_view(), name='tags_list'),
    path("create/", TagCreateView.as_view(), name='tags_create'),
    path("<int:pk>/update/", TagUpdateView.as_view(), name='tags_update'),
    path("<int:pk>/delete/", TagDeleteView.as_view(), name='tags_delete'),
]