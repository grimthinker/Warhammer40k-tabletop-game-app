from typing import TYPE_CHECKING

import pygame
from pygame import Surface, SurfaceType

from dc import Position, Offset
from game_models import BaseModel
from utils import length, distance_w, find_correction, find_correction_circle

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


    def check_collision(self, another_obj: 'BaseObject'):
        current_distance = 0
        limit = 10000
        if isinstance(another_obj, Line) and isinstance(self, Circle):
            limit = self.radius
            current_distance = distance_w(another_obj.position, another_obj.end, self.position)
        if isinstance(another_obj, Circle) and isinstance(self, Circle):
            limit = another_obj.radius + self.radius
            current_distance = length(another_obj.position, self.position)
        if isinstance(another_obj, Rectangle) and isinstance(self, Circle):
            for line in another_obj.lines:
                pass
        return current_distance <= limit, current_distance

    def correct_length_move(self, correct_length: int | None = None):
        move = correct_length if correct_length else self.model.profile.M
        length = self.dragging_line.length
        m = move / (length + 0.00001)
        start_x, start_y = self.dragging_line.position
        end_x, end_y = self.dragging_line.end
        d_x = end_x - start_x
        d_y = end_y - start_y
        return [(start_x + d_x * m), (start_y + d_y * m)]

    def noncollide_position(self, collided_object, current_distance):
        correct_length_move = 0
        if isinstance(self, Circle) and isinstance(collided_object, Line):
            over = self.radius - current_distance
            correction = find_correction(over, self.dragging_line, collided_object)
            correct_length_move = self.dragging_line.length - abs(correction)
        if isinstance(self, Circle) and isinstance(collided_object, Circle):
            error = self.radius + collided_object.radius - current_distance
            correction = find_correction_circle(error, self.radius, collided_object.radius)
            correct_length_move = self.dragging_line.length - abs(correction)
        return self.correct_length_move(correct_length_move)



class Line(BaseObject):
    def __init__(self, end: tuple[float, float], **kwargs):
        super().__init__(**kwargs)
        self.start = self.position
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
        self.dragging_line = Line(color=color, position=position, end=position)
        return self.dragging_line
