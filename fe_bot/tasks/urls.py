from django.urls import path
from .views import TaskWiew

app_name = 'tasks'
urlpatterns = [
    path('tasks/', TaskWiew.as_view()),
]
