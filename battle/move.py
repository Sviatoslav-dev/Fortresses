import time


class Move:
    def __init__(self):
        self.player = None
        self.selected_unit_pos = None
        self.unit_pointers = []
        self.time = time.time()
        self.timeout = 30
