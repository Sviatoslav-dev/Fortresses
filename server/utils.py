import random

from server.cell_types import CellTypes


def create_matrix(wight, height):
    res = []

    for i in range(height):
        res.append([])
        for j in range(wight):
            if i > 0 and j > 0:
                r = random.randint(0, 20)
                if r < 17:
                    res[-1].append(CellTypes.grass.value)
                elif 17 <= r < 20:
                    res[-1].append(CellTypes.water.value)
                else:
                    res[-1].append(CellTypes.gold.value)
            else:
                res[-1].append(CellTypes.grass.value)
    return res
