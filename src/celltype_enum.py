from enum import Enum


class celltype_e(Enum):
    GENERATOR = 0
    CWSPINNER_ALT = 1
    CCWSPINNER_ALT = 2
    MOVER = 3
    SLIDE = 4
    BLOCK = 5
    WALL = 6
    ENEMY = 7
    TRASH = 8

    # may change

    BGDEFAULT = 9
    BGPLACEABLE0 = 10
