from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from partner_program.admin import admin_site

urlpatterns = [
    url(r'^', include('django_telegrambot.urls')),
    path('admin/', admin.site.urls),
    path('admin2/', admin_site.urls),
    url('api/v1/tasks/', include('tasks.urls')),
    url('api/v1/', include('users.urls')),
]
