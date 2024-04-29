# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer

class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print(text_data)  # 在這裡處理接收到的消息

    async def send(self, text_data):
        await self.send(text_data)
