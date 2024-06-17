from django.urls import path
from .views import (PostAPIView,
                    LikeAPIView,
                    CommentCreateAPIView,
                    CommentsByPostAPIView,
                    PostByIdAPIView)

urlpatterns = [
    path('post/<int:post_id>/', PostByIdAPIView.as_view(), name='get-post-by-id'),
    path('posts/<int:pk>/', PostAPIView.as_view(), name='get-posts'),
    path('posts/create/', PostAPIView.as_view(), name='post-create'),
    path('posts/<int:pk>/delete/', PostAPIView.as_view(), name='post-delete'),
    path('posts/like/<int:pk>/', LikeAPIView.as_view(), name='like'),
    path('comment/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('posts/<int:post_id>/comments/', CommentsByPostAPIView.as_view(), name='get-comments-post' )
]