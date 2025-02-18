import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from time import sleep
from random import randint
from django.template import Template,Context

class WSconsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(1000):
            self.send(json.dumps({'message':randint(1,100)}))
            sleep(1)


# User
class Notificationconsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('notification',self.channel_name)
    async def disconnect(self,code):
        await self.channel_layer.group_discard('notification',self.channel_name)

    async def receive(self,text_data):
        text_json_data=json.loads(text_data)
        message=text_json_data['message']
        print(f"Received user message: {message}") 

        await self.send(text_data=json.dumps({
                "message": f"Your request has been sent to the admin: {message}"
            }))    
        await self.channel_layer.group_send(
                'admin-notification', {
                    'type': 'admin_notification',
                    'message': message,
                }
            )

        
    async def send_notification(self,event):
        message=event["message"]

        template=Template('<div class="notification"><p>{{message}}</p></div>')
        context=Context({"message":message})
        renderd_notification=template.render(context)

        await self.send(
            text_data=json.dumps(
                {
                    "type":"notification",
                    "message":renderd_notification
                }
            )
        )


class AdminNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('admin-notification',self.channel_name)

    async def disconnect(self, code):
        await self.channel_layer.group_discard('admin-notification',self.channel_name)
        
    async def admin_notification(self, event):
        # Receive the notification message from the group
        message = event['message']
        await self.send(text_data=json.dumps({
            "message": message
        }))       