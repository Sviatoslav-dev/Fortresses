import asyncio
import json
import time

from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedError

from db.requests import db
from server.player import Player
from server.utils import create_matrix

app = FastAPI()

opponents = {}


class LoginData(BaseModel):
    login: str
    password: str


@app.get("/user")
async def player_user(user_id: int = 70):
    print("USER_id: ", user_id)
    return db.get_user(user_id)


@app.get("/player_units/")
async def player_units(user_id: int = 70):
    print("USER_id: ", user_id)
    units = db.get_user_units(user_id)
    res = {}
    for unit in units:
        unit_type = unit["unit_type"]
        del unit["unit_type"]
        res[unit_type] = unit
    return res


@app.get("/update_unit")
async def update_unit(user_id: int = 1, unit_type: str = "swordsman", skill: str = "heath"):
    db.update_unit_skill(user_id, unit_type, skill)
    return {"result": "success"}


@app.get("/update_unit_stars")
async def update_unit_stars(user_id: int = 1):
    db.add_user_stars(user_id, 10)
    return {"result": "success"}


@app.get("/open_unit")
async def open_unit(user_id: int = 1, unit_type: str = "swordsman"):
    db.open_unit(user_id, unit_type)
    return {"result": "success"}


@app.post("/login")
async def login(login_data: LoginData):
    user_id = db.login(login_data.login, login_data.password)
    return {"id": user_id}


@app.post("/register")
async def register(login_data: LoginData):
    user_id = db.create_user_with_default_units(login_data.login, login_data.password)
    return {"id": user_id}


@app.websocket("/{user_id}/ws")
async def websocket_endpoint(websocket: WebSocket, user_id):
    global opponents
    player = Player(websocket)
    player.user_id = user_id
    opponents[player] = None

    await websocket.accept()

    while not opponents[player]:
        await asyncio.sleep(0.1)

        for plyr in opponents.keys():
            if plyr is not player and not opponents[plyr]:
                print("OPPONENTS: ", len(opponents.keys()))
                opponents[plyr] = player
                opponents[player] = plyr
                player.num = 1
                plyr.num = 2
                field = create_matrix(20, 15)
                player.field = field
                plyr.field = field

    await player.websocket.send_text(json.dumps({
        "action": "setplayer",
        "data": {
            "player": player.num,
        },
    }))

    await player.websocket.send_text(json.dumps({
        "action": "field",
        "data": player.field,
    }))

    units = db.get_user_units(opponents[player].user_id)
    opponent_units = {}
    for unit in units:
        unit_type = unit["unit_type"]
        del unit["unit_type"]
        opponent_units[unit_type] = unit

    await player.websocket.send_text(json.dumps({
        "action": "opponent",
        "data": opponent_units,
    }))

    player.move = True
    player.move_start = time.time()

    opponents[player].move = False
    opponents[player].move_start = time.time()

    while True:
        try:
            timeout = 30
            t = time.time()
            if t - player.move_start > timeout and t - opponents[player].move_start > timeout:
                print("TIMEOUT")
                await player.websocket.send_text(json.dumps({
                    "action": "nextmove",
                }))
                await opponents[player].websocket.send_text(json.dumps({
                    "action": "nextmove",
                }))
                player.move = not player.move
                player.move_start = time.time()

                opponents[player].move = not opponents[player].move
                opponents[player].move_start = time.time()
            else:
                data = await player.websocket.receive_text()
                print(json.loads(data)["action"])
                if json.loads(data)["action"] == "nextmove":
                    player.move = not player.move
                    player.move_start = time.time()

                    opponents[player].move = not opponents[player].move
                    opponents[player].move_start = time.time()
                elif json.loads(data)["action"] == "win":
                    db.update_user_rating(player.user_id, 10)
                # print(f"{sender_log} IN", data)
                await opponents[player].websocket.send_text(data)
        except WebSocketDisconnect:
            break
        except ConnectionClosedError:
            break
