import math
import pygame
from pygame.math import Vector2


class Enemy:
    imgs = []

    def __init__(self, x, y, width, height, path):
        # x and y will be initialized to path[0]
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.animation_count = 0
        self.max_health = 100
        self.health = self.max_health
        self.velocity = Vector2(0, 0)
        self.max_speed = 1
        self.path = path
        self.path_pos = 0
        self.img = None
        self.was_hit = False

    def draw(self, window):
        self.img = self.imgs[self.animation_count]
        self.animation_count += 1
        health_bar_height = 3

        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        surface = pygame.Surface((self.width, self.height + health_bar_height), pygame.SRCALPHA)
        surface.blit(self.img, (0, 0))

        # Create and draw health bar if enemy is not full HP
        if self.health != self.max_health:
            h_bar = self.create_health_bar(health_bar_height)
            surface.blit(h_bar, (0, self.height))

        if self.was_hit:
            dmged_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            dmged_surface.set_alpha(40)
            pygame.draw.rect(dmged_surface, (255, 0, 0), pygame.Rect(0, 0, self.width, self.height))
            surface.blit(dmged_surface, (0, 0))
            self.was_hit = False

        window.blit(surface, (self.x - int(self.width/2), self.y - int(self.height/2)))

    def create_health_bar(self, height):
        """
        Creates health_bar on pygame.Surface
        :param height: health bar height
        :return: Surface to be attached at the bottom-left corner of an enemy
        """
        s = pygame.Surface((self.width, 5))
        health_perc = self.health / self.max_health
        l = int(self.width * health_perc)
        pygame.draw.rect(s, (255, 0, 0), pygame.Rect(0, 0, self.width, height))
        pygame.draw.rect(s, (0, 255, 0), pygame.Rect(0, 0, l, height))
        return s

    def move(self):
        if self.path_pos + 1 >= len(self.path):
            return False
        target = Vector2(*self.path[self.path_pos + 1])
        current = Vector2(self.x, self.y)
        heading = target - current
        distance = heading.magnitude()  # Distance to target
        heading.normalize_ip()
        if distance <= 5:
            self.path_pos += 1

        self.velocity = heading * self.max_speed
        self.x += self.velocity.x
        self.y += self.velocity.y
        return True

    def position_after(self, mag):
        target = Vector2(*self.path[self.path_pos + 1])
        current = Vector2(self.x, self.y)
        heading = target - current
        heading.normalize_ip()

        velocity = heading * self.max_speed * mag
        return current+velocity

    def distance_to(self, x2, y2):
        """
        Distance from enemy to (x2, y2)
        :param x2: x coordinate
        :param y2: y coordinate
        :return: distance
        """
        return math.sqrt((self.x - x2) ** 2 + (self.y - y2) ** 2)

    def hit(self, damage):
        self.health -= damage
        self.was_hit = True
        return self.health <= 0

    def collide(self, pos, radius):
        if self.distance_to(*pos) < radius + self.width/2:
            return True
        return False

    def get_pos(self):
        return self.x, self.y

