from django.urls import path
from .views import TaskWiew, TaskWiewIp

app_name = 'tasks'
urlpatterns = [
    path('tasks/', TaskWiew.as_view()),
    path('tasks_ip/', TaskWiewIp.as_view()),
]
