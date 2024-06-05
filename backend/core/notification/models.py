from django.db import models
from profiles.models import UserProfile


class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('friend_request', 'Friend Request'),
    )

    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='recipient')
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sender')
    type = models.CharField(choices=NOTIFICATION_TYPES, max_length=20)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient}: {self.message}"