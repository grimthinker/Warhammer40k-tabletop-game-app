import math
from dataclasses import dataclass


@dataclass
class GameParams:
    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int
    SCALE: int
    FPS: int


@dataclass
class Position:
    x: int = 0
    y: int = 0
    z: int = 0


@dataclass
class Offset(Position):
    @property
    def distance(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    @property
    def full_distance(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))

