# urls.py
from django.urls import path
from .views import SendDiscordMessageAPIView

urlpatterns = [
    path('send_report', SendDiscordMessageAPIView.as_view(), name='discord_webhook'),
]