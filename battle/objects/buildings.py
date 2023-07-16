import pygame

from battle.game import game
from battle.objects.base_object import BaseObject
from battle.sprites.action_buttons import BuyBuilder, BuySwordsMan


class Building(BaseObject):
    def __init__(self, player):
        super().__init__(player)


class Fortress(Building, pygame.sprite.Sprite):
    action_buttons = [BuyBuilder(370, 550, 25), BuySwordsMan(430, 550, 25)]

    def __init__(self, player):
        super().__init__(player)
        super(Fortress, self).__init__(player)
        print(self.color)
        self.color = (100, 100, 100)
        self.player = player

        self.surf = pygame.Surface((15, 15))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

    async def move_click(self, current_cell):
        if self.player == game.move.player:
            self.do_buttons_active()
            game.remove_unit_pointers()
        else:
            game.remove_unit_pointers()
            game.ui.remove_action_buttons()

    def draw(self):
        game.screen.blit(self.surf, self.rect)


class Road(Building, pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(player)
        super(Road, self).__init__(player)
        self.color = (200, 200, 50)
        self.player = player

        self.surf = pygame.Surface((15, 15))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

    def draw(self):
        game.screen.blit(self.surf, self.rect)


class Mine(Building, pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__(player)
        super(Mine, self).__init__(player)
        self.color = (100, 100, 0)
        self.player = player

        self.player.move_price += 15

        self.surf = pygame.Surface((15, 15))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect()

    def __del__(self):
        self.player.move_price -= 15

    def draw(self):
        game.screen.blit(self.surf, self.rect)
