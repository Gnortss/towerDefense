import pygame
import constants as const
import time


class Defense:
    img = None

    def __init__(self, _level, width, height):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = height
        self.level = 0
        self.damage = 25
        self.range = const.CELL_WIDTH * 2.5  # In pixels
        self.upgrade_cost = []
        self.sell_cost = []
        self.placed = False
        self.selected = True
        self._level = _level
        self.last_attack_time = time.time()
        self.attack_speed = 0.5

    def draw(self, window):
        top_left_x = (self.x - self.width//2) * const.CELL_WIDTH
        top_left_y = (self.y - self.height//2) * const.CELL_HEIGHT

        if self.selected:
            if not self.placed and not self._level.is_in_valid_spot(self):
                color1 = (255, 0, 0)
                color2 = (255, 100, 100)
            else:
                color1 = (0, 0, 255)
                color2 = (100, 100, 255)

            sw = int(self.range * 2)
            sh = sw
            cx = int(self.x * const.CELL_WIDTH + const.CELL_WIDTH//2)
            cy = int(self.y * const.CELL_HEIGHT + const.CELL_HEIGHT//2)
            nx = cx - sw // 2
            ny = cy - sh // 2
            surface = pygame.Surface((sw, sh))
            surface.set_colorkey((0, 0, 0))
            surface.set_alpha(80)
            pygame.draw.circle(surface, color1, (sw // 2, sh // 2), int(self.range) - 2)
            pygame.draw.circle(surface, color2, (sw // 2, sh // 2), int(self.range), 3)
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

    def attack(self, enemies):
        pass

    def upgrade(self):
        pass

    def sell(self):
        pass

    def set_last_attack_time(self, t):
        self.last_attack_time = t

    def get_center_coordinates(self):
        cx = self.x * const.CELL_WIDTH + const.CELL_WIDTH/2
        cy = self.y * const.CELL_HEIGHT + const.CELL_HEIGHT/2
        return cx, cy
