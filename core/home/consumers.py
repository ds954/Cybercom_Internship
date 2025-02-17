import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from time import sleep
from random import randint

class WSconsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        for i in range(1000):
            self.send(json.dumps({'message':randint(1,100)}))
            sleep(1)

class Notificationconsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add('notification',self.channel_name)
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard('notification',self.channel_name)


