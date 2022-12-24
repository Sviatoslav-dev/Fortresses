from objects.base_object import BaseObject


class Building(BaseObject):
    def __init__(self, player):
        super().__init__(player)


class Fortress(Building):
    def __init__(self, player):
        super().__init__(player)
        self.color = (100, 100, 100)


class Road:
    pass


class Mine:
    pass
