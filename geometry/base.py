from typing import TYPE_CHECKING

from basic_data.dc import Offset
from utils import length

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
            size: float = 0
    ):
        self.color = color
        self.position = position
        self.position_z = position_z
        self.line_wide = line_wide
        self.model = model
        self.dragging = False
        self.dragging_lines: list[Line] = list()
        self.last_move_line: Line | None = None
        self.move_lines: list[Line] = list()
        self.to_draw = True
        self.size = size

    @property
    def last_dragging_line(self):
        return self.dragging_lines[-1]

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

    def make_dragging_line(self, color: tuple[int, int, int], position: tuple[int, int]):
        line = Line(color=color, position=position, start=position, end=position)
        self.dragging_lines.append(line)
        return line

