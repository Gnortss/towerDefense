import pygame
import os
from defense import Defense
from defense_type import DefenseType
import constants as const
import time
from projectile import Projectile
from pygame.math import Vector2


class TurretTower(Defense):
    img = None

    def __init__(self, _level):
        super(TurretTower, self).__init__(_level, 3, 3)
        self.type = DefenseType.TOWER
        self.cost = 200
        self.damage = 75
        self.range = const.CELL_WIDTH * 6
        self.upgrade_cost = [300, 500]
        self.sell_cost = [100, 300, 500]
        # Load image
        self.img = pygame.image.load(os.path.join('images/defenses/', 'tower.png')).convert_alpha()
        self.img = pygame.transform.scale(self.img, (self.width * const.CELL_WIDTH, self.height * const.CELL_HEIGHT))
        self.attack_speed = 1
        self.last_attack_time = time.time()
        self.projectiles = []

    def draw(self, window):
        super().draw(window)

        # Move and draw projectiles
        # remove the dead ones
        to_del = []
        for p in self.projectiles:
            if not p.move(window):
                to_del.append(p)
        for p in to_del:
            self.projectiles.remove(p)

    def attack(self, enemies):
        if time.time() - self.last_attack_time < self.attack_speed:
            return False
        cx, cy = self.get_center_coordinates()

        attack = None
        for enemy in enemies:
            if enemy.collide((cx, cy), self.range):
                attack = enemy
                break

        if attack is None:
            return False

        # Shoot projectile towards enemy
        # also shoot slightly ahead of the enemy (based on their speed)

        # heading = Vector2(*self.get_center_coordinates()) - Vector2(*attack.get_pos())
        # heading = heading + attack.velocity

        self.projectiles.append(Projectile(self.get_center_coordinates(), attack.get_pos(), 5))
        self.last_attack_time = time.time()
        return True

    def check_projectile_collisions(self, enemies):
        to_del = []
        for projectile in self.projectiles:
            for enemy in enemies:
                if enemy.collide(projectile.position, projectile.radius):
                    self._level.hit(enemy, self.damage)
                    to_del.append(projectile)
        for p in to_del:
            if p in self.projectiles:
                self.projectiles.remove(p)
