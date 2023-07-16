from typing import List

import pygame

from battle.cell_types import CellTypes, CellColors
from battle.custom_events import GRASS_CLICK


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

    async def on_click(self, pos):
        if self.rect.collidepoint(pos):
            if len(self.objects) == 0:
                pygame.event.post(pygame.event.Event(GRASS_CLICK))
            else:
                clicked_object = self.objects[-1]
                await clicked_object.move_click(self)
