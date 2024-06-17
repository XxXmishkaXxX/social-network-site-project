from django.urls import path
from .views import AllPostsAPIView, FriendsPostsAPIView, SubscriptionsPostsAPIView

urlpatterns = [
    path('posts/all/', AllPostsAPIView.as_view(), name='all-posts'),
    path('posts/friends-posts/', FriendsPostsAPIView.as_view(), name='friends-posts'),
    path('posts/subscriptions-posts/', SubscriptionsPostsAPIView.as_view(), name='subscriptions-posts'),
]
