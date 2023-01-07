from typing import List

import pygame

from actions import buy_builder
from cell_types import CellTypes
from move import Move
from objects.buildings import Building, Mine, Road
from objects.units import Builder, SwordsMan
from socket_client import ws
from sprites.cell_sprites import Cell


class ActionButton(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super(ActionButton, self).__init__()
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.color = (200, 100, 100)
        self.radius = radius
        self.active = False


class BuyBuilder(ActionButton):
    def __init__(self, x, y, radius):
        super(BuyBuilder, self).__init__(x, y, radius)

    async def on_click(self, pos, player, cells):
        if self.rect.collidepoint(pos) and self.active:
            buy_builder(player, cells)
            await ws.send(f"create_0_0_builder")
            return True
        else:
            return False


class BuySwordsMan(ActionButton):
    def __init__(self, x, y, radius):
        super(BuySwordsMan, self).__init__(x, y, radius)
        self.color = (200, 100, 255)

    def on_click(self, pos, player, cells):
        print(player.gold)
        if self.rect.collidepoint(pos) and self.active:
            swords_man_price = 20
            if player.gold >= swords_man_price:
                player.gold -= swords_man_price
                cells[player.fortress_pos[0]][player.fortress_pos[1]].objects.append(
                    SwordsMan(player)
                )
            return True
        else:
            return False


class BuildMine(ActionButton):
    def __init__(self, x, y, radius):
        super(BuildMine, self).__init__(x, y, radius)
        self.color = (200, 200, 100)

    def on_click(self, pos, player, cells: List[List[Cell]], move: Move):
        if self.rect.collidepoint(pos) and self.active:
            mine_price = 40
            cell = cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]]
            if cell.type == CellTypes.gold:
                there_is_mine = False
                for obj in cell.objects:
                    if isinstance(obj, Mine):
                        there_is_mine = True

                if not there_is_mine and player.gold >= mine_price:
                    cell.objects.insert(-2, Mine(player))
                    player.gold -= mine_price

            return True
        else:
            return False


class BuildRoad(ActionButton):
    def __init__(self, x, y, radius):
        super(BuildRoad, self).__init__(x, y, radius)
        self.color = (200, 50, 100)

    def on_click(self, pos, player, cells: List[List[Cell]], move: Move):
        if self.rect.collidepoint(pos) and self.active:
            road_price = 20
            cell = cells[move.selected_unit_pos[0]][move.selected_unit_pos[1]]
            if cell.type == CellTypes.grass:
                there_is_road = False
                for obj in cell.objects:
                    if isinstance(obj, Road):
                        there_is_road = True

                if not there_is_road and player.gold >= road_price:
                    cell.objects.insert(-2, Road(player))
                    player.gold -= road_price

            return True
        else:
            return False
