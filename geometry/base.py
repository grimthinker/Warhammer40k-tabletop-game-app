import math
from typing import TYPE_CHECKING

import pygame
from pygame import Surface, SurfaceType

from dc import Position, Offset
from game_models import BaseModel
from utils import length, distance_w, find_correction_circle, find_angle

if TYPE_CHECKING:
    from main import GameLoop


class BaseObject:
    def __init__(
            self,
            position: tuple[int, int],
            color: tuple[int, int, int] = (0, 0, 0),
            position_z: int = 0,
            line_wide: int = 1,
            model: BaseModel | None = None
    ):
        self.color = color
        self.position = position
        self.position_z = position_z
        self.line_wide = line_wide
        self.model = model
        self.dragging = False
        self.dragging_line: Line | None = None
        self.to_draw = True
        if model:
            self.size = model.profile.base_diameter / 2
        else:
            self.size = 0

    @property
    def draggable(self):
        if self.model:
            return self.model.draggable
        return False


    def draw(self, loop: 'GameLoop'):
        raise NotImplemented

    def set_pos(self, position: tuple[int, int], use_offset=False):
        raise NotImplemented

    def check_point(self, position: tuple[int]):
        raise NotImplemented

    def make_dragging_line(self, color: tuple[int, int, int], position: tuple[int, int]):
        raise NotImplemented


class Line(BaseObject):
    def __init__(self, start: tuple[float, float], end: tuple[float, float], **kwargs):
        super().__init__(**kwargs)
        self.start = start
        self.position = self.start
        self.end = end

    def check_point(self, position: tuple[float, float]):
        return False  # The default line class is not clickable

    def set_pos(self, position: tuple[float, float], use_offset=False):
        self.end = position  # Only changes the end point of the line. Offset is not applied

    def set_line_pos(self, start: tuple[float, float], end: tuple[float, float]):
        self.start = start
        self.end = end

    @property
    def vector(self):
        ax, ay = self.start
        bx, by = self.end
        return bx - ax, by - ay

    @property
    def length(self):
        return length(self.start, self.end)


class Rectangle(BaseObject):
    def __init__(self, angle, **kwargs):
        super().__init__(**kwargs)
        self.angle: float = angle



class Circle(BaseObject):
    def __init__(self, offset: Offset | None = None, **kwargs):
        super().__init__(**kwargs)
        self.offset = offset if offset else Offset(0, 0)
        self.radius = self.size


    def set_pos(self, position: tuple[float, float], use_offset=False):
        point_x, point_y = position
        if use_offset:
            self.position = (point_x + self.offset.x, point_y + self.offset.y)
        else:
            self.position = (point_x, point_y)

    def check_point(self, position: tuple[int, int]) -> bool:
        point_x, point_y = position
        self_x, self_y = self.position
        offset = Offset(self_x - point_x, self_y - point_y)
        if offset.distance < self.radius:
            self.offset = offset
            return True
        else:
            return False

    def make_dragging_line(self, color: tuple[int, int, int], position: tuple[int, int]):
        self.dragging_line = Line(color=color, position=position, start=position, end=position)
        return self.dragging_line

