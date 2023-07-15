import pygame

from battle.custom_events import GRASS_CLICK
from battle.objects.base_object import BaseObject
from battle.sprites.cell_sprites import remove_unit_pointers


class Building(BaseObject):
    def __init__(self, player):
        super().__init__(player)


class Fortress(Building):
    def __init__(self, player):
        super().__init__(player)
        self.color = (100, 100, 100)
        self.player = player

    async def move_click(self, current_cell, move, cells, action_buttons):
        if move.player.fortress_pos == (current_cell.j, current_cell.i):
            # pygame.event.post(pygame.event.Event(FORTRESS_CLICK))
            action_buttons["build_mine"].active = False
            action_buttons["build_road"].active = False
            action_buttons["buy_builder"].active = True
            action_buttons["buy_swords_man"].active = True
            remove_unit_pointers(move, cells)
        else:
            pygame.event.post(pygame.event.Event(GRASS_CLICK))


class Road(Building):
    def __init__(self, player):
        super().__init__(player)
        self.color = (200, 200, 50)
        self.player = player


class Mine(Building):
    def __init__(self, player):
        super().__init__(player)
        self.color = (100, 100, 0)
        self.player = player

        self.player.move_price += 15

    def __del__(self):
        self.player.move_price -= 15
