from typing import List

import numpy as np
import pygame

from cell_types import CellTypes, CellColors, cell_color_by_cell_type
from objects.buildings import Fortress
from sprites.cell_sprites import Cell


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = (20, 15)
        # self.matrix: List[List[List[CellTypes]]] = [[[CellTypes.grass]
        #                                              for _ in range(self.size[1])]
        #                                             for _ in range(self.size[0])]
        self.cells_group = self.create_cells()
        self.__cells: List[List[Cell]] = []
        self.fill_cells_matrix()
        # self.fill_matrix()
        self.paint_cells()

    @property
    def cells(self):
        return self.__cells

    def fill_cells_matrix(self):
        j = -1
        for i, cell in enumerate(self.cells_group.sprites()):
            if i % self.size[1] == 0:
                j += 1
                self.__cells.append([])

            self.__cells[j].append(cell)

    def create_cells(self):
        cells_group = pygame.sprite.Group()
        blockSize = 40
        for j in range(self.size[0]):
            for i in range(self.size[1]):
                cell = Cell(j * blockSize, i * blockSize, blockSize, j, i)
                cells_group.add(cell)

        return cells_group

    def fill_matrix(self, player1, player2):
        self.cells[3][4].type = CellTypes.water
        self.cells[2][4].type = CellTypes.water
        self.cells[3][5].type = CellTypes.water
        self.cells[2][3].type = CellTypes.water
        self.cells[5][2].type = CellTypes.water
        self.cells[10][10].type = CellTypes.water

        self.cells[4][-4].type = CellTypes.gold
        self.cells[7][-3].type = CellTypes.gold
        self.cells[18][-13].type = CellTypes.gold
        self.cells[14][-12].type = CellTypes.gold

        self.cells[-1][0].objects.append(Fortress(player1))
        self.cells[0][-1].objects.append(Fortress(player2))

    def paint_cells(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                if len(self.__cells[x][y].objects) == 0:
                    self.__cells[x][y].color = cell_color_by_cell_type(self.cells[x][y].type).value
                else:
                    self.__cells[x][y].color = self.__cells[x][y].objects[-1].color
