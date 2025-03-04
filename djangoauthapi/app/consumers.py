import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BorrowRequestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = f"user_{self.scope['user'].id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def status_update(self, event):
        await self.send(text_data=json.dumps({
            "status": event["status"],
            "book": event["book"]
        }))
    async def cancel_request(self, event):
        """Handles book cancellation requests."""
        self.send(text_data=json.dumps({
            "type": "cancel_request",
            "status": event["status"],
            "book": event["book"]
        }))    