import asyncio

import pygame

from battle.game_controller import GameController
from battle.socket_client import ws


async def main():
    game = GameController()
    # global ws
    # ws = WebSocket()
    await ws.connect()
    # loop = asyncio.get_event_loop()
    pygame.display.set_caption("pygame+asyncio")
    # pygame_loop = game.pygame_event_loop(loop, asyncio.Queue())
    await game.run()
    await ws.close()


# if __name__ == '__main__':
#     asyncio.run(main())
