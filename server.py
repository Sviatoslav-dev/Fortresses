from fastapi import FastAPI, WebSocket

app = FastAPI()

wss = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global wss
    wss.append(websocket)

    await websocket.accept()
    if len(wss) > 1:
        await wss[0].send_text("setplayer_1")
        await wss[1].send_text("setplayer_2")

    while True:
        sender = websocket
        # sender_log = None
        # receiver = websocket
        data = await sender.receive_text()
        if len(wss) > 1:
            if websocket is wss[0]:
                receiver = wss[1]
                sender_log = "SENDER1"
            else:
                receiver = wss[0]
                sender_log = "SENDER2"

            print(f"{sender_log} IN", data)
            await receiver.send_text(data)