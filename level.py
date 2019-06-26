import pygame
import os
import json
import time
from map import Map
import constants as const
from creeper import Creeper
from turret_tower import TurretTower
from spikes_trap import SpikesTrap
from cell_type import CellType
from defense_type import DefenseType


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
        self.wait_before_spawning = 3
        self.current_wave = 0
        self.paused = True
        self.paused_at = time.time()
        self.placing = None

    def update(self):
        if not self.paused:
            # Move enemies and delete the ones that are at the end of a path
            to_del = []
            for enemy in self.enemies:
                if not enemy.move():
                    to_del.append(enemy)
            for enemy in to_del:
                self.enemies.remove(enemy)
                self.lives -= 1
            # Check if we have to spawn an enemy
            self.spawn_next_enemy()
            print(self.lives)
        # Clip defense which the player is placing to the nearest cell
        if self.placing is not None:
            self.placing.move_to(*pygame.mouse.get_pos())

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
        self.enemies_spawned = 0
        self.last_spawn_time = time.time()
        self.current_wave = 0
        self.paused = True
        self.paused_at = time.time()
        self.placing = None

    def draw(self, window):
        window.blit(self.bg, (0, 0))
        # Draw objects on the map (path, obstacles)
        self.map.draw(window)
        # Draw enemies
        for enemy in reversed(self.enemies):
            enemy.draw(window)

        # Draw defenses
        for defense in self.defenses:
            defense.draw(window)

        # Draw defense which is currently placing
        if self.placing is not None:
            self.placing.draw(window)

    def spawn_next_enemy(self):
        if self.enemies_spawned == 0 and time.time() - self.last_spawn_time < self.wait_before_spawning:
            return

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

    def create_defense(self, defense_id):
        if self.placing is not None:
            return False

        if defense_id == 1:
            self.placing = TurretTower(self)

            if self.placing.cost > self.coins:
                # TODO: notify player that he hasn't got enough coins
                self.placing = None
                return False
        elif defense_id == 2:
            self.placing = SpikesTrap(self)

            if self.placing.cost > self.coins:
                # TODO: notify player that he hasn't got enough coins
                self.placing = None
                return False

        return True

    def confirm_placing(self):
        if self.placing is None:  # Can't confirm if player isn't placing anything
            return False
        if not self.is_in_valid_spot(self.placing):  # Returns false when defense is not in a valid spot
            # print("Not a valid spot")
            return False

        # Set cell types where defense will be placed
        sx, sy = self.placing.x - (self.placing.width // 2), self.placing.y - (self.placing.height // 2)
        for i in range(0, self.placing.width):
            for j in range(0, self.placing.height):
                if self.placing.type == DefenseType.TOWER:
                    self.map.set_cell_type(sx + i, sy + j, CellType.TOWER)
                elif self.placing.type == DefenseType.TRAP:
                    self.map.set_cell_type(sx + i, sy + j, CellType.TRAP)

        self.placing.place()
        self.defenses.append(self.placing)
        # print("Coins: ", self.coins, "-->", self.coins - self.placing.cost)
        self.coins -= self.placing.cost
        self.placing = None
        return True

    def cancel_placing(self):
        if self.placing is None:
            return False
        self.placing = None
        return True

    def is_in_valid_spot(self, defense):
        is_valid = True
        sx, sy = defense.x - (defense.width // 2), defense.y - (defense.height // 2)
        for i in range(0, defense.width):
            for j in range(0, defense.height):
                # print(sx + i, sy + j, self.map.get_cell_type(sx + i, sy + j))
                if defense.type == DefenseType.TOWER and self.map.get_cell_type(sx + i, sy + j) != CellType.FREE:
                    is_valid = False
                elif defense.type == DefenseType.TRAP and self.map.get_cell_type(sx + i, sy + j) != CellType.PATH:
                    is_valid = False
        return is_valid

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


