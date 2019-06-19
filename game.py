import json
from map import Map


class Game:

    def __init__(self, filename):
        self.level_config_file = filename
        with open(filename) as file:
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

    def run(self):
        pass

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

