from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

#половина уже не используется

urlpatterns = [
    url(r'^', include('django_telegrambot.urls')),
    path('admin/', admin.site.urls),
    url('api/v1/tasks/', include('tasks.urls')),
    url('api/v1/', include('users.urls')),
]
