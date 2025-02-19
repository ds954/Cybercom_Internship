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

# NormalClosure	1000	
# (1000) The connection has closed after the request was fulfilled.

# EndpointUnavailable	1001	
# (1001) Indicates an endpoint is being removed. Either the server or client will become unavailable.

# ProtocolError	1002	
# (1002) The client or server is terminating the connection because of a protocol error.

# InvalidMessageType	1003	
# (1003) The client or server is terminating the connection because it cannot accept the data type it received.

# Empty	1005	
# No error specified.

# InvalidPayloadData	1007	
# (1007) The client or server is terminating the connection because it has received data inconsistent with the message type.

# PolicyViolation	1008	
# (1008) The connection will be closed because an endpoint has received a message that violates its policy.

# MessageTooBig	1009	
# (1009) The client or server is terminating the connection because it has received a message that is too big for it to process.

# MandatoryExtension	1010	
# (1010) The client is terminating the connection because it expected the server to negotiate an extension.

# InternalServerError	1011	
# (1011) The connection will be closed by the server because of an error on the server.
# User
class Notificationconsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('notification',self.channel_name)
    async def disconnect(self,code):
        print(f"Disconnect code: {code}")
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