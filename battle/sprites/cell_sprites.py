from typing import List

import pygame

from battle.cell_types import CellTypes, CellColors
from battle.custom_events import GRASS_CLICK
from battle.objects.buildings import Fortress, Road
from battle.objects.unit_pointer import UnitPointer
from battle.objects.units import Builder, SwordsMan
from battle.socket_client import ws


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
                cell = cells[cell_pos[0]][cell_pos[1]]
                if ((cell.type == CellTypes.grass or
                     cell.type == CellTypes.gold) and
                    len(cell.objects) == 0) or \
                        isinstance(cell.objects[-1], Road) or (
                        (isinstance(cell.objects[-1], SwordsMan) or isinstance(cell.objects[-1],
                                                                               Builder)) and
                        cell.objects[-1].player is not move.player and isinstance(clicked_object, SwordsMan)
                ):
                    unit_pointer = UnitPointer(clicked_object, (cell_pos[0], cell_pos[1]))
                    cells[cell_pos[0]][cell_pos[1]].objects.append(unit_pointer)
                    move.unit_pointers.append(unit_pointer)
            except IndexError:
                pass

    async def on_click(self, pos, move, cells, action_buttons):
        if self.rect.collidepoint(pos):
            if len(self.objects) == 0:
                pygame.event.post(pygame.event.Event(GRASS_CLICK))
                action_buttons["build_mine"].active = False
                action_buttons["build_road"].active = False
                remove_unit_pointers(move, cells)
            else:
                clicked_object = self.objects[-1]
                if isinstance(clicked_object, Fortress):
                    if move.player.fortress_pos == (self.j, self.i):
                        # pygame.event.post(pygame.event.Event(FORTRESS_CLICK))
                        action_buttons["build_mine"].active = False
                        action_buttons["build_road"].active = False
                        action_buttons["buy_builder"].active = True
                        action_buttons["buy_swords_man"].active = True
                        remove_unit_pointers(move, cells)
                    else:
                        pygame.event.post(pygame.event.Event(GRASS_CLICK))
                elif isinstance(clicked_object, Builder) and clicked_object.player is move.player:
                    pygame.event.post(pygame.event.Event(GRASS_CLICK))
                    remove_unit_pointers(move, cells)

                    move.selected_unit_pos = (self.j, self.i)
                    if clicked_object.steps > 0:
                        remove_unit_pointers(move, cells)
                    self.create_unit_pointers(clicked_object, move, cells)

                    if cells[move.selected_unit_pos[0]][
                        move.selected_unit_pos[1]].type == CellTypes.gold:
                        action_buttons["build_mine"].active = True
                    else:
                        action_buttons["build_mine"].active = False

                    if cells[move.selected_unit_pos[0]][
                        move.selected_unit_pos[1]].type == CellTypes.grass:
                        action_buttons["build_road"].active = True
                    else:
                        action_buttons["build_road"].active = False
                elif isinstance(clicked_object, SwordsMan) and clicked_object.player is move.player:
                    pygame.event.post(pygame.event.Event(GRASS_CLICK))
                    remove_unit_pointers(move, cells)

                    move.selected_unit_pos = (self.j, self.i)
                    remove_unit_pointers(move, cells)
                    if clicked_object.steps > 0:
                        self.create_unit_pointers(clicked_object, move, cells)
                elif isinstance(clicked_object, UnitPointer):
                    pygame.event.post(pygame.event.Event(GRASS_CLICK))
                    can_go = True

                    selected_unit = \
                        cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects[-1]

                    if isinstance(selected_unit, Builder):
                        if (cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].type
                                == CellTypes.gold):
                            action_buttons["build_mine"].active = True
                        else:
                            action_buttons["build_mine"].active = False

                        if cells[move.selected_unit_pos[0]][
                            move.selected_unit_pos[1]].type == CellTypes.grass:
                            action_buttons["build_road"].active = True
                        else:
                            action_buttons["build_road"].active = False
                    elif isinstance(selected_unit, SwordsMan):
                        if len(self.objects) > 1:
                            if (isinstance(self.objects[-2], SwordsMan) or
                                    isinstance(self.objects[-2], Builder)):
                                self.objects[-2].health -= selected_unit.damage
                                print("DAMAGE: ", self.objects[-2].health)
                                if self.objects[-2].health <= 0:
                                    self.objects[-2].player.units.remove(self.objects[-2])
                                    del self.objects[-2]
                                    selected_unit.steps -= 1
                                else:
                                    can_go = False

                    if can_go:
                        remove_unit_pointers(move, cells)
                        selected_unit_num = len(cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects) - 1
                        cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]].objects.pop(-1)
                        prev_pos = move.selected_unit_pos
                        move.selected_unit_pos = (self.j, self.i)
                        remove_unit_pointers(move, cells)
                        self.objects.append(selected_unit)

                        if selected_unit.steps > 0:
                            self.create_unit_pointers(selected_unit, move, cells)
                            if not object_in_cell(cells[clicked_object.pos[0]][clicked_object.pos[1]],
                                                  Road):
                                selected_unit.steps -= 1
                        await ws.send(f"replace_{prev_pos[0]}_{prev_pos[1]}_{selected_unit_num}_{self.j}_{self.i}")
