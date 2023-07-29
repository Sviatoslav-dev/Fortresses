from enum import Enum, auto


class CellTypes(Enum):
    grass = 1
    water = 2
    gold = 3


class CellColors(Enum):
    grass = (50, 200, 25)
    water = (0, 0, 255)
    gold = (255, 255, 0)
