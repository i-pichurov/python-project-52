"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from task_manager import views
from django.contrib.auth.views import LoginView, LogoutView
from task_manager.user.views import CustomLoginView, CustomLogoutView

urlpatterns = [
    path("", views.index, name='main_page'),
    path("login/", CustomLoginView.as_view(), name='login'),
    path("logout/", CustomLogoutView.as_view(next_page='main_page'), name='logout'),
    path("users/", include("task_manager.user.urls")),
    path("statuses/", include("task_manager.status.urls")),
    path("tasks/", include("task_manager.task.urls")),
    path("tags/", include("task_manager.tag.urls")),
    path("admin/", admin.site.urls),
]
