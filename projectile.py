import pygame
import constants as const
from pygame.math import Vector2
import time


class Projectile:

    def __init__(self, pos, target, speed=1):
        self.radius = 5
        self.spawned = time.time()
        self.lifetime = 4  # in seconds
        self.position = Vector2(*pos)
        self.velocity = Vector2(0, 0)
        self.heading = Vector2(*target) - self.position
        self.heading.normalize_ip()
        self.speed = speed

    def move(self, window):
        if time.time() - self.spawned > self.lifetime:
            return False

        self.velocity = self.heading * self.speed
        self.position += self.velocity
        self.draw(window)
        return True

    def draw(self, window):
        s = pygame.Surface((self.radius, self.radius), pygame.SRCALPHA)
        pygame.draw.circle(s, (50, 50, 50), (self.radius//2, self.radius//2), self.radius)
        window.blit(s, self.position)
