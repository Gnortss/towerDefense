import pygame
import constants as const


class Defense:
    img = None

    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.level = 0
        self.range = 30  # In pixels
        self.upgrade_cost = []
        self.sell_cost = []
        self.placed = False
        self.selected = True

    def draw(self, window):
        top_left_x = (self.x - self.width//2) * const.CELL_WIDTH
        top_left_y = (self.y - self.height//2) * const.CELL_HEIGHT

        if self.selected:
            sw = int(self.range * 2)
            sh = sw
            cx = int(self.x * const.CELL_WIDTH + const.CELL_WIDTH//2)
            cy = int(self.y * const.CELL_HEIGHT + const.CELL_HEIGHT//2)
            nx = cx - sw // 2
            ny = cy - sh // 2
            surface = pygame.Surface((sw, sh))
            surface.set_colorkey((0, 0, 0))
            surface.set_alpha(128)
            pygame.draw.circle(surface, (230, 0, 0), (sw // 2, sh // 2), int(self.range) - 2)
            pygame.draw.circle(surface, (230, 100, 100), (sw // 2, sh // 2), int(self.range), 3)
            window.blit(surface, (nx, ny))

        window.blit(self.img, (top_left_x, top_left_y))

    def move_to(self, x, y):
        """
        Clips the tower to the cell which is covering given x and y
        :param x: x coordinate
        :param y: y coordinate
        :return: None
        """
        self.x = x // const.CELL_WIDTH
        self.y = y // const.CELL_HEIGHT

    def place(self):
        self.placed = True

    def upgrade(self):
        pass

    def sell(self):
        pass
