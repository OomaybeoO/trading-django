from channels.generic.websocket import AsyncWebsocketConsumer
import json
import asyncio
import websockets

class ChatConsumer(AsyncWebsocketConsumer):
    clients = set()  # 用于跟踪所有连接的客户端
    subscription_task = None  # 用于跟踪订阅任务

    async def connect(self):
        await self.accept()
        self.clients.add(self)  # 将当前连接的客户端添加到列表中
        if not self.subscription_task:  # 检查是否已经订阅
            self.subscription_task = asyncio.create_task(self.subscribe_to_other_server())

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
        except json.JSONDecodeError:
            print("Handle JSON decode error")
            # Handle JSON decode error
            pass
        except KeyError:
            print(" Handle missing 'message' key")
            # Handle missing 'message' key
            pass

    async def disconnect(self, close_code):
        self.clients.remove(self)  # 当连接断开时，从列表中移除客户端
        if not self.clients:  # 如果当前没有客户端连接，取消订阅任务
            self.subscription_task.cancel()

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
            # 循环接收消息
            while True:
                try:
                    data = await asyncio.wait_for(websocket.recv(), timeout=5)  # 设置超时时间
                    await self.broadcast(data)  # 广播消息给所有客户端

                     # 解析 JSON 資料
                    parsed_data = json.loads(data)

                    # 從解析後的資料中讀取 lastPr 的值
                    if 'data' in parsed_data and parsed_data['data']:
                        last_pr = parsed_data['data'][0].get('lastPr')
                        # print("Last Price:", last_pr)

                except asyncio.TimeoutError:
                    pass  # 在超时时继续循环，继续接收消息
                except websockets.ConnectionClosed:
                    break  # 如果连接关闭，退出循环
