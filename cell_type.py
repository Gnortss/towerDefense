from enum import Enum


class CellType(Enum):
    DISABLED = 0
    FREE = 1
    PATH = 2
    TOWER = 3
    TRAP = 4
    OBSTACLE = 5
    TAKEN = 6
