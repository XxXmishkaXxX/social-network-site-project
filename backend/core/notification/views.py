from rest_framework import viewsets
from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(recipient=self.request.user.userprofile)
    


class NotificationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)


class NotificationBulkDeleteAPIView(generics.DestroyAPIView):
    serializer_class = NotificationSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user.userprofile
        return Notification.objects.filter(recipient=user)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class MarkNotificationsAsReadAPIView(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        user = self.request.user.userprofile
        unread_notifications = Notification.objects.filter(recipient=user, read=False)
        unread_notifications.update(read=True)
        return Response(status=status.HTTP_200_OK)