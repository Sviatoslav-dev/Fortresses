from objects.base_object import BaseObject


class Building(BaseObject):
    def __init__(self, player):
        super().__init__(player)


class Fortress(Building):
    def __init__(self, player):
        super().__init__(player)
        self.color = (100, 100, 100)


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
