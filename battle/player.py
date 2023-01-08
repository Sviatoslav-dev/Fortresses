class Player:
    def __init__(self, fortress_pos):
        self.gold = 100
        self.fortress_pos = fortress_pos
        self.move_price = 0
        self.units = []
        self.units_data = {}
        # self.mines = []

    def next_move(self):
        self.gold += self.move_price

        for unit in self.units:
            unit.steps = 5
