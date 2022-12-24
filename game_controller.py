from typing import Union

import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from custom_events import FORTRESS_CLICK, GRASS_CLICK
from field import Field
from move import Move
from player import Player
from sprites.action_buttons import BuyBuilder
from objects.units import Unit


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
        self.buy_builder = BuyBuilder(400, 550, 25)
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
                if self.buy_builder.on_click(pygame.mouse.get_pos(),
                                             self.move.player, self.field.cells):
                    continue

                for cell in self.field.cells_group.sprites():
                    cell.on_click(pygame.mouse.get_pos(), self.move, self.field.cells)

            if event.type == FORTRESS_CLICK:
                self.buy_builder.active = True

            if event.type == GRASS_CLICK:
                self.buy_builder.active = False

    def draw(self):
        self.screen.fill((255, 255, 255))

        self.field.paint_cells()
        for cell in self.field.cells_group:
            pygame.draw.rect(self.screen, cell.color, cell, width=0)
            pygame.draw.rect(self.screen, cell.border_color, cell, width=1)

        if self.buy_builder.active:
            pygame.draw.circle(self.screen, self.buy_builder.color,
                               self.buy_builder.rect.center, self.buy_builder.radius)

        pygame.display.flip()

    def next_move(self):
        if self.move.player is self.player1:
            self.move.player = self.player2
        else:
            self.move.player = self.player1
