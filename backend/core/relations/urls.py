from django.urls import path
from .views import (FriendListAPIView, FriendRequestCreateAPIView,
                     SentFriendRequestsView, ReceivedFriendRequestsView, 
                     AcceptFriendRequestAPIView, RejectFriendRequestAPIView, 
                     CheckFriendStatus)

urlpatterns = [
    path('friends/', FriendListAPIView.as_view(), name='friend-list'),
    path('send-friend-requests/', FriendRequestCreateAPIView.as_view(), name='friend-request-create'),
    path('sent-requests/', SentFriendRequestsView.as_view(), name='sent_friend_requests'),
    path('received-requests/', ReceivedFriendRequestsView.as_view(), name='received_friend_requests'),
    path('accept-friend-request/<int:pk>/', AcceptFriendRequestAPIView.as_view(), name='accept_friend_request'),
    path('cancel-friend-request/<int:pk>/', RejectFriendRequestAPIView.as_view(), name='cancel_friend_request'),
    path('check-friend-status/<int:user_id>/', CheckFriendStatus.as_view(), name='check_friend_status'),
]

