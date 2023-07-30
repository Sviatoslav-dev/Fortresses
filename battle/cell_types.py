from enum import Enum, auto


class CellTypes(Enum):
    grass = 1
    water = 2
    gold = 3


class CellColors(Enum):
    grass = (50, 200, 25)
    water = (0, 0, 255)
    gold = (50, 200, 25)#(255, 255, 0)


def cell_color_by_cell_type(cell_type):
    return {
        CellTypes.grass: CellColors.grass,
        CellTypes.water: CellColors.water,
        CellTypes.gold: CellColors.gold,
    }[cell_type]
