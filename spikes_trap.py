import pygame
import os
from defense import Defense
from defense_type import DefenseType
import constants as const


class SpikesTrap(Defense):
    img = None

    def __init__(self, _level):
        super(SpikesTrap, self).__init__(_level, 1, 1)
        self.type = DefenseType.TRAP
        self.range = const.CELL_WIDTH * 1.5
        self.cost = 100
        self.upgrade_cost = []
        self.sell_cost = [50]
        # Load image
        self.img = pygame.image.load(os.path.join('images/defenses/', 'trap.png')).convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width * const.CELL_WIDTH, self.height * const.CELL_HEIGHT))

    def attack(self):
        pass
