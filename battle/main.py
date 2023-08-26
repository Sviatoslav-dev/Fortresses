import os
os.chdir('..')

import asyncio

import pygame

from battle.game_controller import GameController
from battle.socket_client import ws


async def main(user_id):
    gc = GameController(user_id)
    # global ws
    # ws = WebSocket()
    await ws.connect(user_id)
    # loop = asyncio.get_event_loop()
    pygame.display.set_caption("Fortresses")
    # pygame_loop = game.pygame_event_loop(loop, asyncio.Queue())
    await gc.run()
    print("DISCONNECT")
    await ws.close()
    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main(70))
