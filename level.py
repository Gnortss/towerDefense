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
        self.end_message = ''
        self.allow_spawning = True

    def update(self, window):
        # Check if the game ended
        if self.game_ended():
            return self.end_message

        # Check if it's the end of a wave and there are no enemies in the game
        # Pause the game
        if len(self.enemies) == 0 and not self.allow_spawning:
            self.current_wave += 1
            self.allow_spawning = True
            self.last_spawn_time = time.time()
            self.pause()

        if self.paused:
            # update defenses last attack time so they don't start attacking right after unpause
            for defense in self.defenses:
                defense.set_last_attack_time(time.time())

        if not self.paused:
            # Attack with defenses
            for defense in self.defenses:
                defense.attack(self.enemies)

            # Move enemies and delete the ones that are at the end of a path
            to_del = []
            for enemy in self.enemies:
                if not enemy.move():
                    to_del.append(enemy)
            for enemy in to_del:
                self.enemies.remove(enemy)
                self.lives -= 1
            for defense in self.defenses:
                if defense.type == DefenseType.TOWER:
                    defense.check_projectile_collisions(self.enemies)

            # Check if we have to spawn an enemy
            self.spawn_next_enemy()
            # print(self.lives)

        # Clip defense which the player is placing to the nearest cell
        if self.placing is not None:
            self.placing.move_to(*pygame.mouse.get_pos())

        # Draw now
        self.draw(window)
        return None

    def game_ended(self):
        # no lives left
        if self.lives <= 0:
            self.end_message = "Ran out of lives. Dead."
            return True

        # no enemies on the field and all of the waves were spawned
        # sum of all enemies
        all_enemies = 0
        for wave in self.waves:
            for group in wave['enemies']:
                all_enemies += group['count']
        # print(self.enemies_spawned, ">=", all_enemies, "and", len(self.enemies) == 0, " --> ", self.enemies_spawned >= all_enemies and not self.enemies, len(self.enemies))
        if self.enemies_spawned >= all_enemies and len(self.enemies) == 0:
            self.end_message = f"level {self.name} completed!"
            return True

        return False

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
        self.end_message = ''
        self.allow_spawning = True

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

        # Draw some info
        font = pygame.font.SysFont('ubuntumono', 50)
        infobar = pygame.Surface((const.INFOBAR_WIDTH, const.INFOBAR_HEIGHT))
        pygame.draw.rect(infobar, (156, 181, 138), pygame.Rect(0, 0, const.INFOBAR_WIDTH, const.INFOBAR_HEIGHT))
        if self.paused:
            pause_text = font.render('PAUSED', True, (0, 0, 0))
            infobar.blit(pause_text, (25, 25))

        # display coins
        coins_text = font.render(f"COINS: {self.coins}", True, (0, 0, 0))
        infobar.blit(coins_text, (25, 80))

        # display lives
        lives_text = font.render(f"LIVES: {self.lives}", True, (0, 0, 0))
        infobar.blit(lives_text, (25, 135))

        # display current wave
        wave_text = font.render(f"WAVE {self.current_wave + 1}/{len(self.waves)}", True, (0, 0, 0))
        infobar.blit(wave_text, (600, 80))

        window.blit(infobar, (0, const.LEVEL_HEIGHT))
    def hit(self, enemy, damage):
        if enemy in self.enemies:
            dead = enemy.hit(damage)
            if dead:  # enemy was killed
                # TODO: death animation : sike
                self.enemies.remove(enemy)

    def spawn_next_enemy(self):
        if not self.allow_spawning:
            return

        # Find the last group we were spawning from
        count = 0
        for i, w in enumerate(self.waves):
            if i >= self.current_wave:
                break
            for g in w['enemies']:
                count += g['count']
        group = 0

        spawned_this_wave = self.enemies_spawned - count
        if spawned_this_wave == 0 and time.time() - self.last_spawn_time < self.wait_before_spawning:
            return

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
        else:  # the end of current wave
            # make sure it's not the last wave
            if self.current_wave + 1 < len(self.waves):
                self.allow_spawning = False

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

