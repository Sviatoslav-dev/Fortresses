from battle.game import game
from battle.objects.base_object import BaseObject
from battle.sprites.action_buttons import BuyBuilder, BuySwordsMan


class Building(BaseObject):
    def __init__(self, player):
        super().__init__(player)


class Fortress(Building):
    action_buttons = [BuyBuilder(370, 550, 25), BuySwordsMan(430, 550, 25)]

    def __init__(self, player):
        super().__init__(player)
        self.color = (100, 100, 100)
        self.player = player

    async def move_click(self, current_cell):
        if game.move.player.fortress_pos == (current_cell.j, current_cell.i):
            # pygame.event.post(pygame.event.Event(FORTRESS_CLICK))
            self.do_buttons_active()
            game.remove_unit_pointers()
        else:
            game.remove_unit_pointers()
            game.ui.remove_action_buttons()


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
