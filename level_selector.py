import pygame
import constants as const
from level import Level
from os import listdir
from os.path import isfile, join


class LevelSelector:

    def __init__(self, levels_folder, window):
        self.levels_folder = levels_folder
        self.level_names = [f for f in listdir(levels_folder) if isfile(join(levels_folder, f))]
        self.level_names.sort()

        self.anchor = (100, 100)
        self.cell = (400, 100)
        self.cols = 2
        self.col_spacing = 50
        self.rows = 4
        self.row_spacing = 20

        self.draw(window)

    def draw(self, window):
        font = pygame.font.SysFont('ubuntumono', 50)

        # draw background
        surface = pygame.Surface((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
        surface.fill((156, 181, 138))

        # draw cells representing levels
        for col in range(0, self.cols):
            cell_surface = pygame.Surface(self.cell)
            for row in range(0, self.rows):
                pygame.draw.rect(cell_surface, (138, 181, 180), pygame.Rect(0, 0, *self.cell))
                x = self.cell[0] * col + self.col_spacing * col + self.anchor[0]
                y = self.cell[1] * row + self.row_spacing * row + self.anchor[1]
                num = row + col * self.rows
                if num < len(self.level_names):
                    level_name = self.level_names[num].replace(".json", "")
                    text_surface = font.render(level_name, True, (0, 0, 0))
                    cell_surface.blit(text_surface, (50, 25))

                surface.blit(cell_surface, (x, y))

        window.blit(surface, (0, 0))

    def get_level(self, x, y):
        # if x & y is inside a cell then return corresponding level
        x -= self.anchor[0]
        y -= self.anchor[1]
        # find row and column numbers
        col = x // (self.cell[0] + self.col_spacing)
        row = y // (self.cell[1] + self.row_spacing)
        # check if mouse is inside the cell (not in between cells)
        if x % (self.cell[0] + self.col_spacing) <= self.cell[0] and y % (self.cell[1] + self.row_spacing) <= self.cell[1]:
            level_name = self.levels_folder + '/' + self.level_names[row + col * self.rows]
            # create Level and return it
            return Level(level_name)
        # else None
        return None

