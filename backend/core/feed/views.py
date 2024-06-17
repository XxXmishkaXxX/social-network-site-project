from rest_framework import generics, permissions, pagination
from wall.models import Post 
from relations.models import Friend, Follower
from wall.serializers import PostWithAuthorSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class PostPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class FriendsPostsAPIView(generics.ListAPIView):
    serializer_class = PostWithAuthorSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        friends = Friend.objects.filter(user=user).values_list('friend_id', flat=True)
        queryset = Post.objects.filter(author_id__in=friends).order_by('-created_at')
        
        if not queryset.exists():
            return Post.objects.none()
    
        return queryset


class SubscriptionsPostsAPIView(generics.ListAPIView):
    serializer_class = PostWithAuthorSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        # Получаем все идентификаторы пользователей, на которых подписан текущий пользователь
        subscriptions = Follower.objects.filter(follower_id=user.id).values_list('user_id', flat=True)
        queryset = Post.objects.filter(author_id__in=subscriptions).order_by('-created_at')
        
        if not queryset.exists():
            return Post.objects.none() 
        
        return queryset
    

class AllPostsAPIView(generics.ListAPIView):
    serializer_class = PostWithAuthorSerializer
    pagination_class = PostPagination
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Post.objects.all().order_by('-created_at')
        
        if not queryset.exists():
            return Post.objects.none()
        
        return queryset
