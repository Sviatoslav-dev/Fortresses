import pygame

from cell_types import CellTypes
from objects.buildings import Building
from objects.units import Builder


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

    def on_click(self, pos, player, cells):
        if self.rect.collidepoint(pos):
            builder_price = 20
            if player.gold >= builder_price:
                player.gold -= builder_price
                cells[player.fortress_pos[0] + 1][player.fortress_pos[1]].objects.append(
                    Builder(player)
                )
            return True
        else:
            return False


