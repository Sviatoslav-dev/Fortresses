from enum import Enum, auto


class CellTypes(Enum):
    grass = 1
    fortress = 2
    water = 3
    gold = 4


class CellColors(Enum):
    grass = (50, 200, 25)
    fortress = (100, 100, 100)
    water = (0, 0, 255)
    gold = (255, 255, 0)


def cell_color_by_cell_type(cell_type):
    return {
        CellTypes.grass: CellColors.grass,
        CellTypes.fortress: CellColors.fortress,
        CellTypes.water: CellColors.water,
        CellTypes.gold: CellColors.gold,
    }[cell_type]
