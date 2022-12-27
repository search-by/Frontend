from django.urls import path, include
from .views import view_message_from_free_kassa


urlpatterns = [
    path('', view_message_from_free_kassa, name="view_message_from_free_kassa")
]
