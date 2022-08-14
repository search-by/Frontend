from django.urls import path
from .views import TaskWiew

app_name = 'tasks'
urlpatterns = [
    path('post_task_status/', TaskWiew.as_view()),
]
