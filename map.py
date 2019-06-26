import pygame
import os
import constants as const
from cell_type import CellType


class Map:
    imgs = {}

    def __init__(self, grid):
        self.imgs['path'] = pygame.image.load(os.path.join('images/textures/path_texture.png'))
        self.imgs['path'] = pygame.transform.scale(self.imgs['path'], (const.CELL_WIDTH - 1, const.CELL_HEIGHT - 1))

        self.grid = []
        self.width = len(grid[0])
        self.height = len(grid)
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                x = j * const.CELL_WIDTH
                y = i * const.CELL_HEIGHT
                self.grid.append({
                    "info": (CellType(cell), 0),
                    "coords": (x, y)
                })

    def get_cell_info(self, x, y):
        return self.grid[y * self.width + x]['info']

    def get_cell_type(self, x, y):
        return self.grid[y * self.width + x]['info'][0]

    def get_cell_coords(self, x, y):
        return self.grid[y * self.width + x]['coords']

    def set_cell(self, x, y, info, coords):
        self.grid[y * self.width + x] = {
            "info": info,
            "coords": coords
        }

    def set_cell_type(self, x, y, type):
        self.grid[y * self.width + x] = {
            "info": (type, self.get_cell_info(x, y)[1]),
            "coords": self.get_cell_coords(x, y)
        }

    def draw(self, window):
        for x in range(0, self.width):
            for y in range(0, self.height):
                t = self.get_cell_type(x, y)
                if t == CellType.PATH or t == CellType.TRAP:
                    window.blit(self.imgs['path'], self.get_cell_coords(x, y))
