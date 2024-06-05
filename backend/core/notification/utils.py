from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notification.models import Notification
from notification.serializers import NotificationSerializer

def send_like_notification(sender, recipient):
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        type='like',
        message=f"Поставил лайк вашей работе")
        

    serializer = NotificationSerializer(notification)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{recipient.pk}",
        {
            'type': 'send_like_notification',
            'notification': serializer.data,  
        }
    )


def send_comment_notification(sender, recipient):
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        type='comment',
        message=f"Прокомментировал вашу работу")
        

    serializer = NotificationSerializer(notification)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{recipient.pk}",
        {
            'type': 'send_comment_notification',
            'notification': serializer.data,  
        }
    )


def send_friend_request_notification(sender, recipient, request_id):
    notification = Notification.objects.create(
        recipient=recipient,
        sender=sender,
        type='friend_request',
        message=f"хочет с вами дружить"
    )

    serializer = NotificationSerializer(notification)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{recipient.pk}",
        {
            'type': 'send_friend_request_notification',
            'notification': {**serializer.data, 'request_id': request_id},
        }
    )