from typing import List

import pygame

from battle.cell_types import CellTypes, CellColors
from battle.custom_events import GRASS_CLICK


# from socket_client import ws


def remove_unit_pointers(move, cells):
    while len(move.unit_pointers) > 0:
        del cells[move.unit_pointers[0].pos[0]][move.unit_pointers[0].pos[1]].objects[-1]
        del move.unit_pointers[0]


def object_in_cell(cell, obj_type):
    for cell_obj in cell.objects:
        if isinstance(cell_obj, obj_type):
            return True
    return False


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, size, j, i):
        super(Cell, self).__init__()
        self.rect = pygame.Rect(x, y, size, size)
        self.color = CellColors.grass.value
        self.border_color = (255, 255, 255)
        self.type = CellTypes.grass
        self.j = j
        self.i = i
        self.objects: List = []

    async def on_click(self, pos, move, cells, action_buttons):
        if self.rect.collidepoint(pos):
            if len(self.objects) == 0:
                self.grass_click(move, cells, action_buttons)
            else:
                clicked_object = self.objects[-1]
                # if (hasattr(clicked_object, "player")
                #     and clicked_object.player is move.player) or not hasattr(clicked_object,
                #                                                              "player"):
                await clicked_object.move_click(self, move, cells, action_buttons)

    def grass_click(self, move, cells, action_buttons):
        pygame.event.post(pygame.event.Event(GRASS_CLICK))
        action_buttons["build_mine"].active = False
        action_buttons["build_road"].active = False
        remove_unit_pointers(move, cells)
