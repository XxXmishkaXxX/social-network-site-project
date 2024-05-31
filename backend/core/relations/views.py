from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Friend, FriendRequest
from .serializers import FriendSerializer, FriendRequestSerializer, SentFriendRequestSerializer, ReceivedFriendRequestSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from copy import deepcopy
from django.db.models import Q
from rest_framework.views import APIView
from django.contrib.auth import get_user_model


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

            # Логика обработки запроса дружбы (например, отправка уведомлений и т.д.)

            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
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
            instance = self.get_object()
            

            if not instance.is_accepted and instance.to_user == request.user:
                # Устанавливаем статус запроса на принятый
                instance.is_accepted = True
                instance.delete()
                # Создаем новую запись друга
                Friend.objects.create(user=request.user, friend=instance.from_user)
                Friend.objects.create(user=instance.from_user, friend=request.user)
                
                return Response({'detail': 'Friend request accepted'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'This friend request has already been accepted or rejected'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'detail': 'An error occurred while accepting the friend request'}, status=status.HTTP_400_BAD_REQUEST)
        

class RejectFriendRequestAPIView(generics.DestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Проверяем, что запрос находится в состоянии ожидания
            if not instance.is_accepted:
                instance.delete()
                return Response({'detail': 'Friend request rejected'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'This friend request has already been accepted or rejected'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'An error occurred while rejecting the friend request'}, status=status.HTTP_400_BAD_REQUEST)
        


class CheckFriendStatus(APIView):
    
    authentication_classes = [TokenAuthentication]

    def get(self, request, user_id):
        try:
            profile_owner = User.objects.get(id=user_id)
            request_user = request.user
            if request_user.is_anonymous:
                return Response({"is_friend": False, "is_request_sent": False}, status=status.HTTP_200_OK)
            
            # Check if the users are friends
            is_friend = Friend.objects.filter(user=request_user, friend=profile_owner).exists() or Friend.objects.filter(user=profile_owner, friend=request_user).exists()
            
            # Check if there is a friend request
            is_request_sent = FriendRequest.objects.filter(from_user=request_user, to_user=profile_owner, is_accepted=False).exists()
            
            return Response({"is_friend": is_friend, "is_request_sent": is_request_sent}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
