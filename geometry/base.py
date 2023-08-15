import math
from typing import TYPE_CHECKING

from basic_data.dc import Offset
from utils import length, find_angle, ang, ang_alt

if TYPE_CHECKING:
    from main import GameLoop


class BaseObject:
    def __init__(
            self,
            position: tuple[int, int],
            color: tuple[int, int, int] = (0, 0, 0),
            position_z: int = 0,
            line_wide: int = 1,
            model: 'GameModel | TerrainModel | None' = None,
            size: float = 0,
            moving_object = None
    ):
        self.color = color
        self.position = position
        self.position_z = position_z
        self.line_wide = line_wide
        self.model = model
        self.dragging = False
        self.dragging_lines: list[Line] = list()
        self.move_lines: list[Line] = list()
        self.move_borders: list[tuple[Line, Line]] = list()
        self.moving_object = moving_object
        self.footprints: list[BaseObject] = list()
        self.show = True
        self.size = size

    @property
    def last_dragging_line(self):
        return self.dragging_lines[-1] if self.dragging_lines else None

    @property
    def last_move_line(self):
        return self.move_lines[-1] if self.move_lines else None

    @property
    def last_move_borders(self):
        return self.move_borders[-1] if self.move_borders else (None, None)

    @property
    def last_footprint(self):
        return self.footprints[-1] if self.footprints else None

    @property
    def owner(self):
        if self.model:
            return self.model.owner
        return None

    @property
    def passable(self):
        if self.model:
            return self.model.passable
        return False

    @property
    def can_be_stood_on(self):
        if self.model:
            return self.model.can_be_stood_on
        return False

    @property
    def draggable(self):
        if self.model:
            return self.model.draggable
        return False

    def draw(self, loop: 'GameLoop'):
        raise NotImplemented

    def set_pos(self, position: tuple[float, float], use_offset=False):
        raise NotImplemented

    def check_point(self, position: tuple[int]):
        raise NotImplemented

    def make_dragging_line(self, color: tuple[int, int, int], position: tuple[int, int]):
        line = Line(color=color, position=position, start=position, end=position)
        self.dragging_lines.append(line)
        return line

    def make_move_line(self, color: tuple[int, int, int], position: tuple[int, int]):
        line = Line(color=color, position=position, start=position, end=position)
        self.move_lines.append(line)
        return line

    def make_footprint(self, color: tuple[int, int, int]):
        req_class = BaseObject
        for cls in [Circle, Line, Rectangle]:
            if isinstance(self, cls):
                req_class = cls
        footprint = req_class(position=self.position, color=color, size=self.size)
        self.footprints.append(footprint)
        return footprint

    def make_move_borders(self, color: tuple[int, int, int], position: tuple[int, int]):
        raise NotImplemented

    def correct_move_borders(self):
        raise NotImplemented


class Line(BaseObject):
    def __init__(self, start: tuple[float, float], end: tuple[float, float], **kwargs):
        super().__init__(**kwargs)
        self.position = start
        self.end = end

    def check_point(self, position: tuple[float, float]):
        return False  # The default line class is not clickable

    def set_pos(self, position: tuple[float, float], use_offset=False):
        self.end = position  # Only changes the end point of the line. Offset is not applied

    def set_line_pos(self, start: tuple[float, float], end: tuple[float, float]):
        self.position = start
        self.end = end

    @property
    def vector(self):
        ax, ay = self.position
        bx, by = self.end
        return bx - ax, by - ay

    @property
    def length(self):
        return length(self.position, self.end)


class Rectangle(BaseObject):
    def __init__(self, angle: float = 0, **kwargs):
        super().__init__(**kwargs)
        self.angle: float = angle
        self.lines: list[Line] = []



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

    def make_move_borders(self, color: tuple[int, int, int], position: tuple[int, int]):
        a = ang(self.last_move_line.vector, (1, 0), full=True)
        r = self.radius
        x0, y0 = self.position
        position1 = x0 + math.sin(a) * r, y0 + math.cos(a) * r
        position2 = x0 - math.sin(a) * r, y0 - math.cos(a) * r
        border1 = Line(color=color, position=position1, start=position1, end=position1)
        border2 = Line(color=color, position=position2, start=position2, end=position2)
        self.move_borders.append((border1, border2))
        return border1, border2

    def correct_move_borders(self):
        a = ang_alt(self.last_move_line.vector)
        r = self.radius
        x0, y0 = self.last_move_line.position
        x1, y1 = self.last_move_line.end
        border1, border2 = self.last_move_borders
        border1.position = x0 + math.sin(a) * r,  y0 + math.cos(a) * r
        border1.end = x1 + math.sin(a) * r,  y1 + math.cos(a) * r
        border2.position = x0 - math.sin(a) * r,  y0 - math.cos(a) * r
        border2.end = x1 - math.sin(a) * r,  y1 - math.cos(a) * r

