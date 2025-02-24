import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.group_name = "notifications"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print("WebSocket Connected Successfully")
        except Exception as e:
            print(f"WebSocket Connection Error: {e}")
            await self.close(code=1011)

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            print(f"WebSocket Disconnected: {close_code}")
        except Exception as e:
            print(f" WebSocket Disconnect Error: {e}")

    async def send_notification(self, event):
        try:
            message = event["message"]
            await self.send(text_data=json.dumps({"message": message}))
            print("✅ WebSocket Message Sent:", message)  # Debugging
        except Exception as e:
            print(f"WebSocket Message Send Error: {e}")
