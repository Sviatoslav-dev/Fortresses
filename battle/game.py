import pygame

from battle.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from battle.field import Field
from battle.move import Move
from battle.player import Player
from battle.ui import UI


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.field = Field(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.player1 = Player((0, self.field.size[1] - 1))
        print((0, self.field.size[1] - 1))
        self.player2 = Player((self.field.size[0] - 1, 0))
        print((self.field.size[0] - 1, 0))
        self.field.fill_matrix(self.player1, self.player2)
        self.move = Move()
        self.move.player = self.player1
        self.current_player = None
        self.opponent = None
        self.move.selected_unit_pos = None
        self.ui = UI(self.screen)
        self.running = True

    def remove_unit_pointers(self):
        unit_pointers = self.move.unit_pointers
        while len(unit_pointers) > 0:
            del self.field.cells[unit_pointers[0].pos[0]][unit_pointers[0].pos[1]].objects[-1]
            del unit_pointers[0]

    def grass_click(self):
        self.ui.remove_action_buttons()
        self.remove_unit_pointers()


game = Game()
