from typing import List

import numpy as np
import pygame

from cell_types import CellTypes, CellColors, cell_color_by_cell_type
from sprites import Cell


class Field:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = (20, 15)
        self.matrix: List[List[CellTypes]] = [[CellTypes.grass for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.cells_group = self.create_cells()
        self.__cells = []
        self.fill_cells_matrix()
        self.fill_matrix()
        self.fill_sells_by_matrix()

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
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                cell = Cell(x * blockSize, y * blockSize, blockSize)
                cells_group.add(cell)

        return cells_group

    def fill_matrix(self):
        self.matrix[-1][0] = CellTypes.fortress
        self.matrix[0][-1] = CellTypes.fortress

        self.matrix[3][4] = CellTypes.water
        self.matrix[2][4] = CellTypes.water
        self.matrix[3][5] = CellTypes.water
        self.matrix[2][3] = CellTypes.water
        self.matrix[5][2] = CellTypes.water
        self.matrix[10][10] = CellTypes.water

        self.matrix[4][-4] = CellTypes.gold
        self.matrix[7][-3] = CellTypes.gold
        self.matrix[18][-13] = CellTypes.gold
        self.matrix[14][-12] = CellTypes.gold

        self.print_matrix()

    def print_matrix(self):
        for row in self.matrix:
            for cell in row:
                print(cell.value, end=" ")
            print()

    def fill_sells_by_matrix(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.__cells[x][y].color = cell_color_by_cell_type(self.matrix[x][y]).value
