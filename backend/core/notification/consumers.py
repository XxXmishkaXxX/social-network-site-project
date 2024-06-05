from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user_id = self.scope['user'].id
            self.group_name = f"notifications_{self.user_id}"  
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def send_like_notification(self, event):
        notification_data = event["notification"]  
        await self.send(text_data=json.dumps(notification_data)) 

    async def send_comment_notification(self, event):
        notification_data = event["notification"]  
        await self.send(text_data=json.dumps(notification_data))

    async def send_friend_request_notification(self, event):
        notification_data = event["notification"] 
        await self.send(text_data=json.dumps(notification_data))

