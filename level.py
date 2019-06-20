import pygame
import os
import json
import time
from map import Map
import constants as const
from creeper import Creeper


class Level:
    imgs = {}

    def __init__(self, filename):

        self.level_config_file = filename
        with open(filename) as file:
            data = json.load(file)
            self.name = data['name']
            self.bg = pygame.image.load(os.path.join('images/backgrounds/', data['background']))
            self.bg = pygame.transform.scale(self.bg, (const.LEVEL_WIDTH, const.LEVEL_HEIGHT))
            self.lives = data['lives']
            self.coins = data['coins']
            self.waves = data['waves']
            self.available_defenses = data['available_defenses']
            self.path = []
            for l in data['path']:
                self.path.append((l[0], l[1]))
            self.map = Map(data['map'])

        self.defenses = []
        self.enemies = []
        self.enemies_spawned = 0
        self.last_spawn_time = time.time()
        self.current_wave = 0
        self.paused = True
        self.paused_at = time.time()

    def update(self):
        if not self.paused:
            # Move enemies
            for enemy in self.enemies:
                enemy.move()
            # Check if we have to spawn an enemy
            self.spawn_next_enemy()

    def reset(self):
        with open(self.level_config_file) as file:
            data = json.load(file)
            self.name = data['name']
            self.lives = data['lives']
            self.coins = data['coins']
            self.waves = data['waves']
            self.available_defenses = data['available_defenses']
            self.path = []
            for l in data['path']:
                self.path.append((l[0], l[1]))
            self.map = Map(data['map'])

        self.defenses = []
        self.enemies = []
        self.current_wave = 0
        self.paused = True

    def draw(self, window):
        window.blit(self.bg, (0, 0))
        # Draw objects on the map (path, obstacles)
        self.map.draw(window)
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(window)

    def spawn_next_enemy(self):
        # Find the last group we were spawning from
        count = 0
        group = 0
        for enemy_group in self.waves[self.current_wave]['enemies']:
            # If already spawned this group then go to next one
            if self.enemies_spawned >= count + enemy_group['count']:
                count += enemy_group['count']
                group += 1
                continue
            else:
                break

        if group < len(self.waves[self.current_wave]['enemies']):
            enemy_group = self.waves[self.current_wave]['enemies'][group]
            if time.time() - self.last_spawn_time >= enemy_group['time_dif'] or self.enemies_spawned == 0:
                if enemy_group['type'] == 'enemy':
                    self.enemies.append(Creeper(*self.path[0], const.CELL_WIDTH, const.CELL_HEIGHT, self.path))
                    self.enemies_spawned += 1
                    self.last_spawn_time = time.time()

    def pause(self):
        self.paused_at = time.time()
        self.paused = True

    def unpause(self):
        self.last_spawn_time += (time.time() - self.paused_at)
        self.paused = False

    def toggle_pause(self):
        if self.paused:
            self.last_spawn_time += (time.time() - self.paused_at)
        else:
            self.paused_at = time.time()
        self.paused = not self.paused


