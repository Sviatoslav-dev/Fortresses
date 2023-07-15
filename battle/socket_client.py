import asyncio
import json

import websockets


class WebSocket:
    def __init__(self):
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect('ws://127.0.0.1:8000/ws')

    async def send(self, msg):
        await self.websocket.send(msg)

    async def recv(self):
        # try:
        #   return self.websocket.messages.get_nowait()
        # except asyncio.queues.QueueEmpty:
        #     pass
        try:
            return await asyncio.wait_for(self.websocket.recv(), timeout=0.01)
        except asyncio.exceptions.TimeoutError:
            return None

    async def close(self):
        await self.websocket.close()

    async def send_command(self, command):
        await self.send(json.dumps(command))


ws = WebSocket()
