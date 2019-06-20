import math


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
        self.velocity = 1.5
        self.path = path
        self.path_pos = 0
        self.img = None

    def draw(self, window):
        self.img = self.imgs[self.animation_count]
        self.animation_count += 1

        if self.animation_count >= len(self.imgs):
            self.animation_count = 0

        window.blit(self.img, (self.x, self.y))

    def move(self):
        if self.path_pos + 1 >= len(self.path):
            return

        dist = math.sqrt((self.x - self.path[self.path_pos + 1][0])**2 + (self.y - self.path[self.path_pos + 1][1])**2)

        if dist < self.velocity:
            self.path_pos += 1

        if self.path_pos + 1 >= len(self.path):
            return

        x1, y1 = self.x, self.y
        x2, y2 = self.path[self.path_pos + 1]

        angle = math.atan2(y2 - y1, x2 - x1)  # In Radians
        if angle < 0:
            angle += 2 * math.pi
        self.x = int(self.x + math.cos(angle) * self.velocity)
        self.y = int(self.y + math.sin(angle) * self.velocity)

    def hit(self, damage):
        self.health -= damage
        return self.health <= 0

    def collide(self):
        pass


