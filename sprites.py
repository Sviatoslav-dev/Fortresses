import pygame

from cell_types import CellTypes, CellColors


class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super(Cell, self).__init__()
        self.rect = pygame.Rect(x, y, size, size)
        self.color = CellColors.grass.value
        self.border_color = (255, 255, 255)
        self.type = CellTypes.grass

    def on_click(self, pos):
        if self.rect.collidepoint(pos):
            pass
            # self.color = (255, 0, 0)
            # print(self.rect)
