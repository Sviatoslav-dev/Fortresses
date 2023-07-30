from typing import List

import pygame

from battle.cell_types import CellTypes, cell_color_by_cell_type
from battle.sprites.cell_sprites import Cell


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

    def fill_matrix(self, matrix):
        for i, _ in enumerate(matrix):
            for j, _ in enumerate(matrix[i]):
                self.cells[j][i].type = CellTypes(matrix[i][j])
                if CellTypes(matrix[i][j]) == CellTypes.water:
                    self.cells[j][i].image = pygame.transform.scale(pygame.image.load("icons/water.png"), (40, 40))
                if CellTypes(matrix[i][j]) == CellTypes.gold:
                    self.cells[j][i].image = pygame.transform.scale(pygame.image.load("icons/gold.png"), (40, 40))

    def paint_cells(self):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.__cells[x][y].color = cell_color_by_cell_type(self.cells[x][y].type).value
