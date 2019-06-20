from enum import Enum


class CellType(Enum):
    DISABLED = 0
    FREE = 1
    PATH = 2
    DEFENSE = 3
    OBSTACLE = 4
    TAKEN = 5
