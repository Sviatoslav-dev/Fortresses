import json

from fastapi import FastAPI, WebSocket

from db.requests import db

app = FastAPI()

wss = []


@app.get("/player_units/")
async def root(user_id: int = 70):
    print("USER_id: ", user_id)
    units = db.get_user_units(user_id)
    res = {}
    for unit in units:
        unit_type = unit["unit_type"]
        del unit["unit_type"]
        res[unit_type] = unit
    return res


@app.get("/update_unit")
async def root(user_id: int = 1, unit_type: str = "swordsman", skill: str = "heath"):
    db.update_unit_skill(user_id, unit_type, skill)
    return {"result": "success"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global wss
    wss.append(websocket)

    await websocket.accept()
    if len(wss) > 1:
        await wss[0].send_text(json.dumps({
            "action": "setplayer",
            "data": {
                "player": 1,
            },
        }))
        await wss[1].send_text(json.dumps({
            "action": "setplayer",
            "data": {
                "player": 2,
            },
        }))

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
