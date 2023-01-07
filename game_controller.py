import asyncio
import select

import pygame

from actions import buy_builder
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from custom_events import GRASS_CLICK, NEXT_MOVE
from field import Field
from move import Move
from player import Player
from socket_client import ws
from sprites.action_buttons import BuyBuilder, BuildMine, BuildRoad, BuySwordsMan
from sprites.buttons import NextMoveButton
from sprites.cell_sprites import remove_unit_pointers


class GameController:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.field = Field(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player1 = Player((0, self.field.size[1] - 1))
        self.player2 = Player((self.field.size[0] - 1, 0))
        self.field.fill_matrix(self.player1, self.player2)
        self.move = Move()
        self.move.player = self.player1
        self.current_player = None
        self.opponent = None

        self.buttons = {
            "next_move": NextMoveButton(750, 580, 10)
        }
        self.buttons["next_move"].active = True

        self.action_buttons = {
            "buy_builder": BuyBuilder(370, 550, 25),
            "buy_swords_man": BuySwordsMan(430, 550, 25),
            "build_mine": BuildMine(370, 550, 25),
            "build_road": BuildRoad(430, 550, 25)
        }
        self.move.selected_unit_pos = None

        self.running = True

    def __del__(self):
        pygame.quit()

    async def parse_action(self, msg):
        tokens = msg.split('_')
        if tokens[0] == 'setplayer':
            print("PLAYER_SETED")
            if tokens[1] == '1':
                print("SETED1")
                self.current_player = self.player1
                self.opponent = self.player2
            else:
                print("SETED2")
                self.current_player = self.player2
                self.opponent = self.player1
        elif tokens[0] == 'replace':
            x1, y1, x2, y2 = int(tokens[1]), int(tokens[2]), int(tokens[4]), int(tokens[5])
            prev_pos = self.field.cells[x1][y1]
            new_pos = self.field.cells[x2][y2]
            print(len(prev_pos.objects))
            new_pos.objects.append(prev_pos.objects[int(tokens[3])])
            del prev_pos.objects[int(tokens[3])]
        elif tokens[0] == 'create':
            if tokens[3] == 'builder':
                buy_builder(self.opponent, self.field.cells)
        elif tokens[0] == 'nextmove':
            await self.next_move()

    async def run(self):
        while self.running:
            await self.events()
            self.draw()
            # if ready[0]:
            #     print("IN ", ws.recv())
            await asyncio.sleep(0.03)
            answ = await ws.recv()
            if answ:
                print("IN ", answ)
                await self.parse_action(answ)
            # self.clock.tick(30)
            # self.pygame_event_loop(loop, event_queue)

    async def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                print("CLICK")
                print(self.move.player)
                print(self.current_player)
                print(self.player2)
                if self.move.player is self.current_player:
                    print("CURRENT PLAYER")
                    if await self.action_buttons["buy_builder"].on_click(pygame.mouse.get_pos(),
                                                                         self.move.player, self.field.cells):
                        continue

                    if self.action_buttons["buy_swords_man"].on_click(pygame.mouse.get_pos(),
                                                                      self.move.player,
                                                                      self.field.cells):
                        continue

                    if self.action_buttons["build_mine"].on_click(pygame.mouse.get_pos(),
                                                                  self.move.player, self.field.cells,
                                                                  self.move):
                        continue

                    if self.action_buttons["build_road"].on_click(pygame.mouse.get_pos(),
                                                                  self.move.player, self.field.cells,
                                                                  self.move):
                        continue

                    if self.buttons["next_move"].on_click(pygame.mouse.get_pos()):
                        continue

                    for cell in self.field.cells_group.sprites():
                        await cell.on_click(pygame.mouse.get_pos(), self.move, self.field.cells,
                                            self.action_buttons)

            # if event.type == FORTRESS_CLICK:
            #     self.buy_builder.active = True

            if event.type == GRASS_CLICK:
                self.action_buttons["buy_builder"].active = False

            if event.type == GRASS_CLICK:
                self.action_buttons["buy_swords_man"].active = False

            if event.type == NEXT_MOVE:
                await self.next_move()
                await ws.send(f"nextmove")

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.field.paint_cells()
        for cell in self.field.cells_group:
            pygame.draw.rect(self.screen, cell.color, cell, width=0)
            pygame.draw.rect(self.screen, cell.border_color, cell, width=1)

        if self.action_buttons["buy_builder"].active:
            pygame.draw.circle(self.screen, self.action_buttons["buy_builder"].color,
                               self.action_buttons["buy_builder"].rect.center,
                               self.action_buttons["buy_builder"].radius)

        if self.action_buttons["buy_swords_man"].active:
            pygame.draw.circle(self.screen, self.action_buttons["buy_swords_man"].color,
                               self.action_buttons["buy_swords_man"].rect.center,
                               self.action_buttons["buy_swords_man"].radius)

        if self.action_buttons["build_mine"].active:
            pygame.draw.circle(self.screen, self.action_buttons["build_mine"].color,
                               self.action_buttons["build_mine"].rect.center,
                               self.action_buttons["build_mine"].radius)

        if self.action_buttons["build_road"].active:
            pygame.draw.circle(self.screen, self.action_buttons["build_road"].color,
                               self.action_buttons["build_road"].rect.center,
                               self.action_buttons["build_road"].radius)

        if self.buttons["next_move"].active:
            pygame.draw.circle(self.screen, self.buttons["next_move"].color,
                               self.buttons["next_move"].rect.center,
                               self.buttons["next_move"].radius)

        pygame.display.flip()

    async def next_move(self):
        print("NEXT MOVE")
        remove_unit_pointers(self.move, self.field.cells)
        self.action_buttons["buy_builder"].active = False
        self.action_buttons["buy_swords_man"].active = False
        self.action_buttons["build_mine"].active = False
        self.action_buttons["build_road"].active = False

        if self.move.player is self.player1:
            self.move.player = self.player2
        else:
            self.move.player = self.player1

        self.move.player.next_move()
