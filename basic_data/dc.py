import math
from dataclasses import dataclass

from pygame.key import ScancodeWrapper

from basic_data.enums import ControlEventTypes


@dataclass
class GameParams:
    SCREEN_WIDTH: int
    SCREEN_HEIGHT: int
    SCALE: float
    FPS: int


@dataclass
class Position:
    x: float = 0
    y: float = 0
    z: float = 0


@dataclass
class Offset(Position):
    @property
    def distance(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    @property
    def full_distance(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2) + math.pow(self.z, 2))


@dataclass
class ControlEvent:
    pos: tuple[float, float]
    type: ControlEventTypes
    data: str | float | dict
    mouse_motion: bool
    keys: ScancodeWrapper
    mouse_pos: tuple[int, int]


@dataclass
class PlayerProfile:
    nickname: str
    password: str = ''
