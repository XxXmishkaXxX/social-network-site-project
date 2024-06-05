from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender_fullname = serializers.SerializerMethodField()
    sender_avatar = serializers.SerializerMethodField()
    sender_id = serializers.SerializerMethodField()

    
    class Meta:
        model = Notification
        fields = ['id','sender_fullname', 'sender_avatar', 'sender_id', 'message', 'type', 'read', 'created_at']


    def get_sender_avatar(self, obj):
        return obj.sender.avatar.url
    
    def get_sender_fullname(self, obj):
        return obj.sender.full_name
    
    def get_sender_id(self, obj):
        return obj.sender.pk