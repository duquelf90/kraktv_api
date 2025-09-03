from django.urls import path
from .views import YouTubeChannelInfoView

urlpatterns = [
    path('channel/<str:channel_id>/', YouTubeChannelInfoView.as_view(), name='youtube-channel-info'),
]