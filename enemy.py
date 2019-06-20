import math
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
        self.health = 100
        self.velocity = Vector2(0, 0)
        self.max_speed = 1
        self.path = path
        self.path_pos = 0
        self.img = None

    def draw(self, window):
        self.img = self.imgs[self.animation_count]
        self.animation_count += 1

        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        window.blit(self.img, (self.x + int(self.width/2), self.y + int(self.height/2)))

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

    def hit(self, damage):
        self.health -= damage
        return self.health <= 0

    def collide(self):
        pass


