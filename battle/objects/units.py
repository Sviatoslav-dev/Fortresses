import pygame

from battle.cell_types import CellTypes
from battle.custom_events import GRASS_CLICK
from battle.objects.base_object import BaseObject
from battle.objects.buildings import Road
from battle.objects.unit_pointer import UnitPointer
from battle.player import Player
from battle.sprites.cell_sprites import remove_unit_pointers


class Unit(BaseObject):
    def __init__(self, player):
        super().__init__(player)

    def create_unit_pointers(self, cell, clicked_object, move, cells):
        for cell_pos in [
            (cell.j + 1, cell.i),
            (cell.j + 1, cell.i + 1),
            (cell.j, cell.i + 1),
            (cell.j - 1, cell.i + 1),
            (cell.j - 1, cell.i),
            (cell.j - 1, cell.i - 1),
            (cell.j, cell.i - 1),
            (cell.j + 1, cell.i - 1),
        ]:
            try:
                cell = cells[cell_pos[0]][cell_pos[1]]
                if ((cell.type == CellTypes.grass or
                     cell.type == CellTypes.gold) and
                    len(cell.objects) == 0) or \
                        isinstance(cell.objects[-1], Road) or (
                        (isinstance(cell.objects[-1], SwordsMan) or isinstance(cell.objects[-1],
                                                                               Builder)) and
                        cell.objects[-1].player is not move.player and isinstance(clicked_object,
                                                                                  SwordsMan)
                ):
                    unit_pointer = UnitPointer(clicked_object, (cell_pos[0], cell_pos[1]))
                    cells[cell_pos[0]][cell_pos[1]].objects.append(unit_pointer)
                    move.unit_pointers.append(unit_pointer)
            except IndexError:
                pass


class SwordsMan(Unit):
    def __init__(self, player: Player):
        super().__init__(player)
        self.health = 100#player.units_data["swords_man"]["health"]#100
        self.damage = 50#player.units_data["swords_man"]["health"]#50
        self.color = (100, 255, 200)
        self.player = player
        self.player.units.append(self)
        self.steps = 5

        self.player.move_price -= 5

    async def move_click(self, current_cell, move, cells, action_buttons):
        pygame.event.post(pygame.event.Event(GRASS_CLICK))
        remove_unit_pointers(move, cells)

        move.selected_unit_pos = (current_cell.j, current_cell.i)
        remove_unit_pointers(move, cells)
        if self.steps > 0:
            self.create_unit_pointers(current_cell, self, move, cells)

    def replace(self, current_cell, move, cells, action_buttons, clicked_object):
        if len(current_cell.objects) > 1:
            if (isinstance(current_cell.objects[-2], SwordsMan) or
                    isinstance(current_cell.objects[-2], Builder)):
                current_cell.objects[-2].health -= self.damage
                print("DAMAGE: ", current_cell.objects[-2].health)
                if current_cell.objects[-2].health <= 0:
                    current_cell.objects[-2].player.units.remove(current_cell.objects[-2])
                    del current_cell.objects[-2]
                    self.steps -= 1
                # else:
                #     can_go = False

    def __del__(self):
        self.player.move_price += 5


class Builder(Unit):
    def __init__(self, player: Player):
        super().__init__(player)
        print(player.units_data)
        self.health = 100#player.units_data["builder"]["health"]#100
        self.color = (255, 100, 200)
        self.player = player
        self.player.units.append(self)
        self.steps = 5

        self.player.move_price -= 5

    async def move_click(self, current_cell, move, cells, action_buttons):
        pygame.event.post(pygame.event.Event(GRASS_CLICK))
        remove_unit_pointers(move, cells)

        move.selected_unit_pos = (current_cell.j, current_cell.i)
        if self.steps > 0:
            remove_unit_pointers(move, cells)
        self.create_unit_pointers(current_cell, self, move, cells)

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

    def replace(self, current_cell, move, cells, action_buttons):
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

    def __del__(self):
        self.player.move_price += 5
