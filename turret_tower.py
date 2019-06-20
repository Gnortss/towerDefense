import pygame
import os
from defense import Defense
import constants as const


class TurretTower(Defense):
    img = None

    def __init__(self):
        super(TurretTower, self).__init__(3, 3)
        self.cost = 200
        self.range = 30
        self.upgrade_cost = [300, 500]
        self.sell_cost = [100, 300, 500]
        # Load image
        self.img = pygame.image.load(os.path.join('images/defenses/', 'tower.png'))
        self.img = pygame.transform.scale(self.img, (self.width * const.CELL_WIDTH, self.height * const.CELL_HEIGHT))

    def attack(self):
        pass
