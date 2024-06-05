from django.urls import path
from .views import NotificationViewSet, NotificationDetailAPIView, NotificationBulkDeleteAPIView, MarkNotificationsAsReadAPIView


urlpatterns = [
    path('get-notifications/', NotificationViewSet.as_view({'get': 'list'})),
    path('delete/<int:pk>/', NotificationDetailAPIView.as_view(), name='notification-detail'),
    path('delete-all/', NotificationBulkDeleteAPIView.as_view(), name='notification-bulk-delete'),
    path('mark-as-read/', MarkNotificationsAsReadAPIView.as_view(), name='mark-notifications-as-read'),
]