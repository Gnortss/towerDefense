import pygame
import os
from defense import Defense
from defense_type import DefenseType
import constants as const
import time


class SpikesTrap(Defense):
    img = None

    def __init__(self, _level):
        super(SpikesTrap, self).__init__(_level, 1, 1)
        self.type = DefenseType.TRAP
        self.range = const.CELL_WIDTH * 1.5
        self.damage = 25
        self.cost = 100
        self.upgrade_cost = []
        self.sell_cost = [50]
        # Load image
        self.img = pygame.image.load(os.path.join('images/defenses/', 'trap.png')).convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width * const.CELL_WIDTH, self.height * const.CELL_HEIGHT))
        self.attack_speed = 0.5
        self.last_attack_time = time.time()

    def attack(self, enemies):
        if time.time() - self.last_attack_time < self.attack_speed:
            return False

        attack = []
        cx, cy = self.get_center_coordinates()
        for enemy in enemies:
            if enemy.collide((cx, cy), self.range):
                attack.append(enemy)

        if len(attack) is 0:
            return False

        for enemy in attack:
            self._level.hit(enemy, self.damage)

        self.last_attack_time = time.time()
        return True
