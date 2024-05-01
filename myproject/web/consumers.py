# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import websockets

class ChatConsumer(AsyncWebsocketConsumer):
    clients = set()  # 用于跟踪所有连接的客户端

    async def connect(self):
        await self.accept()
        self.clients.add(self)  # 将当前连接的客户端添加到列表中
        # await self.subscribe_to_other_server()  # 在连接建立时订阅其他服务器

    async def disconnect(self, close_code):
        self.clients.remove(self)  # 当连接断开时，从列表中移除客户端

    async def subscribe_to_other_server(self):
        async with websockets.connect('wss://ws.bitget.com/v2/ws/public') as websocket:
            # 构建订阅消息
            subscribe_message = {
                "op": "subscribe",
                "args": [
                    {
                        "instType": "SPOT",
                        "channel": "ticker",
                        "instId": "BTCUSDT"
                    }
                ]
            }
            # 发送订阅消息
            await websocket.send(json.dumps(subscribe_message))
            while True:
                data = await websocket.recv()
                # 广播从其他服务器接收到的数据给所有客户端
                await self.broadcast(data)

    async def broadcast(self, data):
        # 广播从其他服务器接收到的数据给所有客户端
        for client in self.clients:
            await client.send(text_data=data)
            
    async def receive(self, text_data):
        try:
            print("收到訊息:",text_data)
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            # Echo back the received message
            await self.send(text_data=json.dumps({
                'message': message
            }))
            print(message)

        except json.JSONDecodeError:
            print("Handle JSON decode error")
            # Handle JSON decode error
            pass
        except KeyError:
            print(" Handle missing 'message' key")
            # Handle missing 'message' key
            pass
