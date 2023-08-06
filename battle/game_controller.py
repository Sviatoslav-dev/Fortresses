import asyncio
import json
import time

import pygame
import requests

from battle.actions import buy_builder, buy_swordsman, buy_road, buy_mine
from battle.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from battle.custom_events import GRASS_CLICK, NEXT_MOVE
from battle.objects.buildings import Fortress
from battle.socket_client import ws
from .cell_types import CellTypes
from .game import game


class GameController:
    def __init__(self, user_id):
        global game
        self.fog_of_war = False
        self.user_id = user_id
        pygame.init()
        game.init()
        game.field.cells[-1][0].objects.append(Fortress(game.player2))
        game.field.cells[0][-1].objects.append(Fortress(game.player1))
        self.clock = pygame.time.Clock()
        self.finding_opponent_text = pygame.font.Font(None, 36).render('Пошук суперника...', 1,
                                                                       (180, 0, 0))
        game.ui.gold = pygame.font.Font(None, 36)
        game.ui.move_timer = pygame.font.Font(None, 36)
        game.running = True
        self.units_data = json.loads(
            requests.get(f'http://127.0.0.1:8000/player_units?user_id={self.user_id}').text)
        print("USRER_DATA: ", self.user_id, self.units_data)

    def __del__(self):
        pygame.quit()

    async def parse_action(self, msg):
        dict_msg = json.loads(msg)
        if dict_msg["action"] == 'setplayer':
            if int(dict_msg["data"]["player"]) == 1:
                print("PLAYER1")
                game.current_player = game.player1
                game.opponent = game.player2
                game.field.cells[0][-1].is_open = True
            else:
                print("PLAYER2")
                game.current_player = game.player2
                game.opponent = game.player1
                game.field.cells[-1][0].is_open = True
            print("SET_UNIT_DATA")
            game.current_player.units_data = self.units_data
            game.current_player.user_id = self.user_id
        elif dict_msg["action"] == 'field':
            game.field.fill_matrix(dict_msg["data"])
        elif dict_msg["action"] == 'opponent':
            game.opponent.units_data = dict_msg["data"]
        elif dict_msg["action"] == 'replace':
            data = dict_msg["data"]
            x1, y1, x2, y2 = int(data["x1"]), int(data["y1"]), int(data["x2"]), int(data["y2"])
            prev_pos = game.field.cells[x1][y1]
            new_pos = game.field.cells[x2][y2]
            new_pos.objects.append(prev_pos.objects[int(data["el"])])
            del prev_pos.objects[int(data["el"])]
        elif dict_msg["action"] == 'create':
            data = dict_msg["data"]
            if dict_msg["data"]["type"] == 'builder':
                buy_builder(game.opponent, game.field.cells)
            if dict_msg["data"]["type"] == 'swordsman':
                buy_swordsman(game.opponent, game.field.cells)
            if dict_msg["data"]["type"] == 'road':
                buy_road(game.opponent, game.field.cells, data["x"], data["y"])
            if dict_msg["data"]["type"] == 'mine':
                buy_mine(game.opponent, game.field.cells, data["x"], data["y"])
        elif dict_msg["action"] == 'nextmove':
            await self.next_move()
        elif dict_msg["action"] == 'attack':
            data = dict_msg["data"]
            cell = game.field.cells[int(data["x"])][int(data["y"])]
            unit = cell.objects[int(data["el"])]
            unit.health -= int(data["damage"])
            if unit.health <= 0:
                if cell.objects[int(data["el"])] in unit.player.units:
                    unit.player.units.remove(cell.objects[int(data["el"])])
                del cell.objects[int(data["el"])]

    async def run(self):
        while game.running:
            await self.events()
            if game.opponent:
                self.draw()
                if time.time() - game.move.time > game.move.timeout:
                    await ws.send_command({"action": "move_timeout"})
                    game.move.time = time.time()
            else:
                self.finding_opponent()
            await asyncio.sleep(0.03)
            answ = await ws.recv()
            if answ:
                print("IN ", answ)
                await self.parse_action(answ)
            # self.clock.tick(30)

    def finding_opponent(self):
        game.screen.fill((255, 255, 255))
        game.screen.blit(self.finding_opponent_text, (SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2))
        pygame.display.flip()

    async def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if game.move.player is game.current_player:
                    for button in game.ui.action_buttons + [game.ui.next_move_button]:
                        if await button.on_click(pygame.mouse.get_pos()):
                            continue

                    for cell in game.field.cells_group.sprites():
                        await cell.on_click(pygame.mouse.get_pos(), game.move)

            if event.type == GRASS_CLICK:
                game.grass_click()

            if event.type == NEXT_MOVE:
                await self.next_move()
                await ws.send(json.dumps({"action": "nextmove", "data": {}}))

    def draw(self):
        game.screen.fill((255, 255, 255))
        game.field.paint_cells()
        for cell in game.field.cells_group:
            if cell.is_open or not self.fog_of_war:
                if cell.type != CellTypes.water:
                    pygame.draw.rect(game.screen, cell.color, cell, width=0)

                if cell.type == CellTypes.water or cell.type == CellTypes.gold:
                    game.screen.blit(cell.image, cell.rect)

                if cell.type != CellTypes.water:
                    pygame.draw.rect(game.screen, cell.border_color, cell, width=1)

                if len(cell.objects) > 0:
                    for obj in cell.objects:
                        obj.rect.center = cell.rect.center
                        obj.draw()
                    # cell.objects[-1].update()
            else:
                pygame.draw.rect(game.screen, (0, 0, 0), cell, width=0)

        timer_color = (255, 0, 0) if game.move.player is game.player2 else (0, 0, 255)
        game.ui.draw(game.current_player.gold, time.time() - game.move.time, timer_color)

        pygame.display.flip()

    async def next_move(self):
        print("NEXT MOVE")
        game.remove_unit_pointers()
        game.ui.remove_action_buttons()

        if game.move.player is game.player1:
            game.move.player = game.player2
        else:
            game.move.player = game.player1

        game.move.player.next_move()
        game.move.time = time.time()
