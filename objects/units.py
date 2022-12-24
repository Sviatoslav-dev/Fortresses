from objects.base_object import BaseObject


class Unit(BaseObject):
    def __init__(self, player):
        super().__init__(player)


class SwordsMan(Unit):
    pass
    # def __init__(self, player):
    #     super().__init__(player)


class Builder(Unit):
    def __init__(self, player):
        super().__init__(player)
        self.color = (255, 100, 200)
