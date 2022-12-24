import weakref
from typing import List

import pygame

from cell_types import CellTypes, CellColors
from custom_events import FORTRESS_CLICK, GRASS_CLICK
from objects.base_object import BaseObject
from objects.buildings import Fortress
from objects.unit_pointer import UnitPointer
from objects.units import Builder


def remove_unit_pointers(move, cells):
    while len(move.unit_pointers) > 0:
        del cells[move.unit_pointers[0].pos[0]][move.unit_pointers[0].pos[1]].objects[-1]
        del move.unit_pointers[0]


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, size, j, i):
        super(Cell, self).__init__()
        self.rect = pygame.Rect(x, y, size, size)
        self.color = CellColors.grass.value
        self.border_color = (255, 255, 255)
        self.type = CellTypes.grass
        self.j = j
        self.i = i
        self.objects: List[BaseObject] = []

    def create_unit_pointers(self, clicked_object, move, cells):
        for cell_pos in [
            (self.j + 1, self.i),
            (self.j + 1, self.i + 1),
            (self.j, self.i + 1),
            (self.j - 1, self.i + 1),
            (self.j - 1, self.i),
            (self.j - 1, self.i - 1),
            (self.j, self.i - 1),
            (self.j + 1, self.i - 1),
        ]:
            try:
                if ((cells[cell_pos[0]][cell_pos[1]].type == CellTypes.grass or
                     cells[cell_pos[0]][cell_pos[1]].type == CellTypes.gold) and
                        len(cells[cell_pos[0]][cell_pos[1]].objects) == 0):
                    unit_pointer = UnitPointer(clicked_object, (cell_pos[0], cell_pos[1]))
                    cells[cell_pos[0]][cell_pos[1]].objects.append(unit_pointer)
                    move.unit_pointers.append(unit_pointer)
            except IndexError:
                pass

    def on_click(self, pos, move, cells):
        if self.rect.collidepoint(pos):
            if len(self.objects) == 0:
                pygame.event.post(pygame.event.Event(GRASS_CLICK))
            else:
                clicked_object = self.objects[-1]
                if isinstance(clicked_object, Fortress):
                    if move.player.fortress_pos == (self.j, self.i):
                        pygame.event.post(pygame.event.Event(FORTRESS_CLICK))
                    else:
                        pygame.event.post(pygame.event.Event(GRASS_CLICK))
                elif isinstance(clicked_object, Builder):
                    pygame.event.post(pygame.event.Event(GRASS_CLICK))

                    move.selected_unit_pos = (self.j, self.i)
                    remove_unit_pointers(move, cells)
                    self.create_unit_pointers(clicked_object, move, cells)

                elif isinstance(clicked_object, UnitPointer):
                    pygame.event.post(pygame.event.Event(GRASS_CLICK))
                    selected_unit = cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects[-1]
                    cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects.pop(-1)
                    move.selected_unit_pos = (self.j, self.i)
                    remove_unit_pointers(move, cells)
                    self.objects.append(selected_unit)
                    self.create_unit_pointers(clicked_object, move, cells)
