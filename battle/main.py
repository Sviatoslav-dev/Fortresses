import os
os.chdir('..')

import asyncio

import pygame

from battle.game_controller import GameController
from battle.socket_client import ws


async def main(user_id):
    gc = GameController(user_id)
    await ws.connect(user_id)
    pygame.display.set_caption("Fortresses")
    await gc.run()
    print("DISCONNECT")
    await ws.close()
    pygame.quit()


if __name__ == '__main__':
    asyncio.run(main(70))
