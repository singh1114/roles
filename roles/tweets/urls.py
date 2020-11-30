from django.urls import path

from tweets.views import TweetView, AdminTweetView, ApproveChange, ReadAuditLogs

urlpatterns = [
    path('my/', TweetView.as_view(), name='my_tweet'),
    path('my/<int:id>/', TweetView.as_view(), name='delete_tweet'),
    path('logs/', ReadAuditLogs.as_view(), name='read_logs'),
    path('approve/', ApproveChange.as_view(), name='awaiting_approval'),
    path('approve/<int:id>/', ApproveChange.as_view(), name='approve'),
    path('user/<int:user_id>/', AdminTweetView.as_view(), name='initiate_tweet'),
    path('user/initiate/<int:id>/', AdminTweetView.as_view(), name='action_initiate'),
]
