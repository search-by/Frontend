from django.urls import path
from .views import LogWiew, PimeyesView
app_name = 'log'
urlpatterns = [
    path('post_log/<int:chat_id>/<str:user_name>/<str:text>/', LogWiew.as_view()),
    path('put_pimeyes/', PimeyesView.as_view()),
]
