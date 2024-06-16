from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notification.models import Notification
from notification.serializers import NotificationSerializer

def send_notification(sender, recipient, type, message):
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        type=type,
        message=message)
        

    serializer = NotificationSerializer(notification)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{recipient.pk}",
        {
            'type': 'send_notification',
            'notification': serializer.data,  
        }
    )





