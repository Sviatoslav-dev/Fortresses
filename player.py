class PlayerMove:
    def __init__(self):
        self.selected_unit = None


class Player:
    def __init__(self):
        self.gold = 100
        self.units = []
        self.mines = []
