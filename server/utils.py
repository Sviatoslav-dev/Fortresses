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
            # res[-1].append(CellTypes.grass.value)

    print(res)

    # res[4][3] = CellTypes.water.value
    # res[4][3] = CellTypes.water.value
    # res[5][2] = CellTypes.water.value
    # res[3][2] = CellTypes.water.value
    # res[2][5] = CellTypes.water.value
    # res[10][10] = CellTypes.water.value
    #
    # res[-4][4] = CellTypes.gold.value
    # res[-3][7] = CellTypes.gold.value
    # res[-13][18] = CellTypes.gold.value
    # res[-12][14] = CellTypes.gold.value
    return res
