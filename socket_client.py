# import websocket
# import rel
# import asyncio
#
#
# def on_message(ws, message):
#     print(message)
#
#
# def on_error(ws, error):
#     print(error)
#
#
# def on_close(ws, close_status_code, close_msg):
#     print("### closed ###")
#
#
# def on_open(ws):
#     print("Opened connection")
#     ws.send("rrrrrrrrrrrrrrrrrrrrr")
#
#
# websocket.enableTrace(True)
# ws = websocket.WebSocketApp("ws://127.0.0.1:8001/ws",
#                             on_open=on_open,
#                             on_message=on_message,
#                             on_error=on_error,
#                             on_close=on_close)
#
#
import asyncio

import websockets
from websocket import create_connection


# ws = None


# async def main():
#     global ws
#     print("HERE")
#     # ws = create_connection("ws://127.0.0.1:8001/ws")
#     ws = await websockets.connect('ws://127.0.0.1:8001/ws')
#     # print(await recv(ws))
#     # print(ws.recv(timeout=0.1))
#     print("Sending 'Hello, World'...")
#     # await ws.send("Hello, World")
#     print("Sent")
#     print("Receiving...")
#     result = await ws.recv()
#     print("Received '%s'" % result)
#     await ws.close()


# asyncio.run(main())

class WebSocket:
    def __init__(self):
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect('ws://127.0.0.1:8001/ws')

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


ws = WebSocket()
