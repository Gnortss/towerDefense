import pygame
import os
from enemy import Enemy


class Creeper(Enemy):

    def __init__(self, x, y, width, height, path):
        super(Creeper, self).__init__(x, y, width, height, path)

        self.img = pygame.image.load(os.path.join('images/enemies/', 'enemy.jpg'))
        self.img = pygame.transform.scale(self.img, (width, height))
        self.imgs = [self.img]

