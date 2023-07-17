import pygame

from battle.actions import buy_builder
from battle.cell_types import CellTypes
from battle.game import game
from battle.socket_client import ws


class ActionButton(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super(ActionButton, self).__init__()
        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)
        self.color = (200, 100, 100)
        self.radius = radius
        self.active = False

    def draw(self, screen):
        pass


class BuyBuilder(ActionButton):
    def __init__(self, x, y, radius):
        super(BuyBuilder, self).__init__(x, y, radius)

    async def on_click(self, pos):
        if self.rect.collidepoint(pos) and self.active:
            buy_builder(game.move.player, game.field.cells)
            await ws.send_command({
                "action": "create",
                "data": {
                    "x": 0,
                    "y": 0,
                    "type": "builder",
                }
            })
            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)


class BuySwordsMan(ActionButton):
    def __init__(self, x, y, radius):
        super(BuySwordsMan, self).__init__(x, y, radius)
        self.color = (200, 100, 255)

    async def on_click(self, pos):
        from battle.objects.units import SwordsMan
        print(game.move.player.gold)
        if self.rect.collidepoint(pos) and self.active:
            swords_man_price = 20
            if game.move.player.gold >= swords_man_price:
                game.move.player.gold -= swords_man_price
                game.field.cells[
                    game.move.player.fortress_pos[0]
                ][game.move.player.fortress_pos[1]].objects.append(
                    SwordsMan(game.move.player)
                )
                await ws.send_command({
                    "action": "create",
                    "data": {
                        "x": 0,
                        "y": 0,
                        "type": "swordsman",
                    }
                })
            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)


class BuildMine(ActionButton):
    def __init__(self, x, y, radius):
        super(BuildMine, self).__init__(x, y, radius)
        self.color = (200, 200, 100)

    async def on_click(self, pos):
        from battle.objects.buildings import Mine
        if self.rect.collidepoint(pos) and self.active:
            mine_price = 40
            cell = game.field.cells[game.move.selected_unit_pos[0]][game.move.selected_unit_pos[1]]
            if cell.type == CellTypes.gold:
                there_is_mine = False
                for obj in cell.objects:
                    if isinstance(obj, Mine):
                        there_is_mine = True

                if not there_is_mine and game.move.player.gold >= mine_price:
                    cell.objects.insert(-2, Mine(game.move.player))
                    game.move.player.gold -= mine_price

            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)


class BuildRoad(ActionButton):
    def __init__(self, x, y, radius):
        super(BuildRoad, self).__init__(x, y, radius)
        self.color = (200, 50, 100)

    async def on_click(self, pos):
        from battle.objects.buildings import Road
        if self.rect.collidepoint(pos) and self.active:
            road_price = 20
            cell = game.field.cells[game.move.selected_unit_pos[0]][game.move.selected_unit_pos[1]]
            if cell.type == CellTypes.grass:
                there_is_road = False
                for obj in cell.objects:
                    if isinstance(obj, Road):
                        there_is_road = True

                if not there_is_road and game.move.player.gold >= road_price:
                    cell.objects.insert(-2, Road(game.move.player))
                    game.move.player.gold -= road_price

            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)
