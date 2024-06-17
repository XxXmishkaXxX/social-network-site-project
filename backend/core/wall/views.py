from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from profiles.models import UserProfile
from profiles.serializers import UserProfileSerializer
from .models import Post, LikePostModel, CommentPostModel
from .serializers import CommentSerializer, PostSerializer, PostWithAuthorSerializer
from notification.utils import send_notification
from django.shortcuts import get_object_or_404



class PostAPIView(APIView):
    
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, )
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(author=user_profile).order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response({'posts': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        data = request.data
        
        data['author'] = request.user.userprofile
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'detail': 'Пост не найден'}, status=status.HTTP_404_NOT_FOUND)

        if post.author != request.user.userprofile:
            return Response({'detail': 'У вас нет прав для удаления этого поста'}, status=status.HTTP_403_FORBIDDEN)

        post.delete()
        return Response({'detail': 'Пост успешно удален'}, status=status.HTTP_200_OK)




class LikeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        user_profile = request.user.userprofile
        post = Post.objects.get(pk=pk)

        try:
            LikePostModel.objects.get(post_id=pk, user_profile=user_profile)

            LikePostModel.objects.filter(post_id=pk, user_profile=user_profile).delete()
            if post.likes_count != 0:
                post.likes_count -= 1
            else:
                post.likes_count = 0
            post.save()
            return Response({'detail': 'Лайк удален', 'likes_count': post.likes_count}, status=status.HTTP_200_OK)

        except LikePostModel.DoesNotExist:
            post.likes_count += 1
            LikePostModel.objects.create(post_id=pk, user_profile=user_profile)
            post.save()

            if request.user.userprofile != post.author:
                send_notification(
                    sender=request.user.userprofile,
                    recipient= post.author,
                    type='like',
                    message='Поставил лайк вашей работе'
                    )

            return Response({'detail': 'Лайк создан', 'likes_count': post.likes_count}, status=status.HTTP_201_CREATED)



class CommentCreateAPIView(APIView):
    
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            
            post_id = request.data.get('post_id')
            text = request.data.get('text')
            post = Post.objects.get(pk=post_id)


            # Создаем комментарий для этого поста
            comment_data = {'post': post_id, 'text': text, "user_profile": request.user.userprofile}
            comment_serializer = CommentSerializer(data=comment_data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                user_profile = UserProfileSerializer(request.user.userprofile, many=False)
                

                if request.user.userprofile != post.author:
                    send_notification(
                        sender=request.user.userprofile,
                        recipient= post.author,
                        type='comment',
                        message='Прокомментировал вашу работу'
                        )
                
                return Response({'comment': comment_serializer.data, 'user_profile':user_profile.data}, status=status.HTTP_201_CREATED)
            
            else:
                return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'detail': 'Пост с указанным ID не существует'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'Произошла ошибка при добавлении комментария'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentsByPostAPIView(APIView):
    
    def get(self, request, post_id, *args, **kwargs):
        try:
            # Получаем все комментарии для указанного поста
            comments = CommentPostModel.objects.filter(post_id=post_id)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except CommentPostModel.DoesNotExist:
            return Response({'detail': 'Комментарии для указанного поста не найдены'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'detail': 'Произошла ошибка при получении комментариев'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class PostByIdAPIView(APIView):
    
    def get(self, request, post_id, *args, **kwargs):
        try:
            # Get the single instance of Post using get_object_or_404
            post = get_object_or_404(Post, id=post_id)
            
            # Serialize the single instance, not the queryset
            serializer = PostWithAuthorSerializer(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({'detail': 'Post с указанным id не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({'detail': 'Произошла ошибка при получении поста'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)