from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Friend, FriendRequest
from .serializers import FriendSerializer, FriendRequestSerializer, SentFriendRequestSerializer, ReceivedFriendRequestSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from copy import deepcopy
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from notification.utils import send_notification
from profiles.models import UserProfile
from .models import Follower
from .serializers import FollowerSerializer
from django.shortcuts import get_object_or_404



User = get_user_model()


class FriendListAPIView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Friend.objects.filter(user=self.request.user)
    
class FriendRequestCreateAPIView(generics.CreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            
            data = deepcopy(request.data)
            data['from_user'] = request.user.id
            serializer = FriendRequestSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            to_user_profile = UserProfile.objects.get(pk=data['to_user'])

            send_notification(
                sender=request.user.userprofile,
                recipient=to_user_profile, 
                type='friend_request',
                message='Хочет с вами дружить')

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class SentFriendRequestsView(generics.ListAPIView):
    serializer_class = SentFriendRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(from_user=user)


class ReceivedFriendRequestsView(generics.ListAPIView):
    serializer_class = ReceivedFriendRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(to_user=user)


class AcceptFriendRequestAPIView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        try:
            from_user_id = request.query_params.get('from_user')
            to_user_id = request.user.id

            friend_request = FriendRequest.objects.get(from_user=from_user_id, to_user=to_user_id)

            if not friend_request.is_accepted and friend_request.to_user == request.user:
                # Устанавливаем статус запроса на принятый
                friend_request.is_accepted = True
                friend_request.delete()

                # Создаем новую запись друга
                Friend.objects.create(user=request.user, friend=friend_request.from_user)
                Friend.objects.create(user=friend_request.from_user, friend=request.user)
                
                send_notification(
                    sender=request.user.userprofile,
                    recipient=UserProfile.objects.get(pk=from_user_id), 
                    type='friend_request',
                    message='Принял(а) ваш запрос в друзья')
                
                return Response({'detail': 'Friend request accepted'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'This friend request has already been accepted or rejected'}, status=status.HTTP_400_BAD_REQUEST)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'detail': 'An error occurred while accepting the friend request'}, status=status.HTTP_400_BAD_REQUEST)

class RejectFriendRequestAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            if request.query_params.get('to_user'): 
                from_user_id = request.user.id
                to_user_id = request.query_params.get('to_user')
            else:
                to_user_id = request.user.id
                from_user_id = request.query_params.get('from_user')
                
            if not to_user_id:
                return Response({'detail': 'To user ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            friend_request = FriendRequest.objects.get(from_user=from_user_id, to_user=to_user_id)

            if not friend_request.is_accepted:
                friend_request.delete()
                return Response({'detail': 'Friend request rejected'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'This friend request has already been accepted or rejected'}, status=status.HTTP_400_BAD_REQUEST)
        except FriendRequest.DoesNotExist:
            return Response({'detail': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': f'An error occurred while rejecting the friend request: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)    

class FollowUserView(generics.CreateAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_to_follow_id = request.data.get('user_id')
        
        try:
            user_to_follow = get_object_or_404(User, id=user_to_follow_id)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        follower, created = Follower.objects.get_or_create(user=user_to_follow, follower=request.user)
        
        if created:
            return Response({"message": "Successfully followed the user."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You are already following this user."}, status=status.HTTP_200_OK)

class UnfollowUserView(generics.DestroyAPIView):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user_to_unfollow_id = request.data.get('user_id')
        user_to_unfollow = User.objects.get(id=user_to_unfollow_id)

        try:
            follower = Follower.objects.get(user=user_to_unfollow, follower=request.user)
            follower.delete()
            return Response({"message": "Successfully unfollowed the user."}, status=status.HTTP_204_NO_CONTENT)
        except Follower.DoesNotExist:
            return Response({"message": "You are not following this user."}, status=status.HTTP_400_BAD_REQUEST)
