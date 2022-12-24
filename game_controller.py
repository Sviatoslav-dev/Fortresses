import pygame

from cell_types import CellColors, CellTypes
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from field import Field
from player import Player


class GameController:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

        self.field = Field(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.running = True

        self.player1 = Player()
        self.player2 = Player()

        self.move = self.player1

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
                for cell in self.field.cells_group.sprites():
                    cell.on_click(pygame.mouse.get_pos())

    def draw(self):
        self.screen.fill((255, 255, 255))

        for cell in self.field.cells_group:
            pygame.draw.rect(self.screen, cell.color, cell, width=0)
            pygame.draw.rect(self.screen, cell.border_color, cell, width=1)

        pygame.display.flip()

    def next_move(self):
        if self.move is self.player1:
            self.move = self.player2
        else:
            self.move = self.player1
