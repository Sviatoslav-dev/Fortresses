import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from custom_events import GRASS_CLICK, NEXT_MOVE
from field import Field
from move import Move
from player import Player
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

    def run(self):
        while self.running:
            self.events()
            self.draw()
            self.clock.tick(30)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                if self.action_buttons["buy_builder"].on_click(pygame.mouse.get_pos(),
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
                    cell.on_click(pygame.mouse.get_pos(), self.move, self.field.cells,
                                  self.action_buttons)

            # if event.type == FORTRESS_CLICK:
            #     self.buy_builder.active = True

            if event.type == GRASS_CLICK:
                self.action_buttons["buy_builder"].active = False

            if event.type == GRASS_CLICK:
                self.action_buttons["buy_swords_man"].active = False

            if event.type == NEXT_MOVE:
                self.next_move()

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

    def next_move(self):
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
