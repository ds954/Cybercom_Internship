import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BorrowRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_group = f"user_{self.scope['user'].id}"  # Unique group for each user
        await self.channel_layer.group_add(self.user_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.channel_layer.group_send(
            self.user_group,
            {
                "type": "update_request",
                "message": data["message"],
            }
        )

    async def update_request(self, event):
        await self.send(text_data=json.dumps({"message": event["message"]}))
