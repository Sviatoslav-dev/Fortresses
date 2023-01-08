from battle.objects.base_object import BaseObject
from battle.player import Player


class Unit(BaseObject):
    def __init__(self, player):
        super().__init__(player)


class SwordsMan(Unit):
    def __init__(self, player: Player):
        super().__init__(player)
        self.health = player.units_data["swords_man"]["health"]#100
        self.damage = player.units_data["swords_man"]["health"]#50
        self.color = (100, 255, 200)
        self.player = player
        self.player.units.append(self)
        self.steps = 5

        self.player.move_price -= 5

    def __del__(self):
        self.player.move_price += 5


class Builder(Unit):
    def __init__(self, player: Player):
        super().__init__(player)
        self.health = player.units_data["builder"]["health"]#100
        self.color = (255, 100, 200)
        self.player = player
        self.player.units.append(self)
        self.steps = 5

        self.player.move_price -= 5

    def __del__(self):
        self.player.move_price += 5
