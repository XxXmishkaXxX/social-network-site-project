from django.urls import path
from .views import (PostAPIView,
                    LikeAPIView,
                    CommentCreateAPIView)

urlpatterns = [
    path('posts/<int:pk>/', PostAPIView.as_view(), name='get-posts'),
    path('posts/create/', PostAPIView.as_view(), name='post-create'),
    path('posts/<int:pk>/delete/', PostAPIView.as_view(), name='post-delete'),
    path('posts/like/<int:pk>/', LikeAPIView.as_view(), name='like'),
    path('comment/create/', CommentCreateAPIView.as_view(), name='comment-create')
]