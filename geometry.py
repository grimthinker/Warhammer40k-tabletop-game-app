import pygame
from pygame import Surface, SurfaceType

from dc import Position, Offset
from game_models import BaseModel


class BaseObject:
    def __init__(
            self,
            color: tuple[int, int, int],
            position: tuple[int, int],
            line_wide: int = 1,
            model: BaseModel | None = None
    ):
        self.color = color
        self.position = position
        self.line_wide = line_wide
        self.model = model
        self.dragging = False
        self.dragging_line = Line | None
        self.to_draw = True

    @property
    def draggable(self):
        if self.model:
            return self.model.draggable
        return False

    def draw(self, screen: Surface | SurfaceType):
        raise NotImplemented

    def set_pos(self, position: tuple[int, int], use_offset=False):
        raise NotImplemented

    def check_collide(self, position: tuple[int]):
        raise NotImplemented

    def make_dragging_line(self, color: tuple[int, int, int], position: tuple[int, int]):
        raise NotImplemented


class Line(BaseObject):
    def __init__(self, end: tuple[int, int], **kwargs):
        super().__init__(**kwargs)
        self.end = end

    def draw(self, screen: Surface | SurfaceType):
        pygame.draw.line(
            screen,
            self.color,
            self.position,
            self.end,
            self.line_wide
        )

    def check_collide(self, position: tuple[int]):
        return False  # The default line class is not clickable

    def set_pos(self, position: tuple[int, int], use_offset=False):
        self.end = position  # Only changes the end point of the line. Offset is not applied


class Circle(BaseObject):
    def __init__(self, radius: int, offset: Offset | None = None, **kwargs):
        super().__init__(**kwargs)
        self.offset = offset if offset else Offset(0, 0)
        self.radius = radius

    def draw(self, screen: Surface | SurfaceType):
        pygame.draw.circle(screen, self.color, self.position, self.radius, self.line_wide)

    def set_pos(self, position: tuple[int, int], use_offset=False):
        point_x, point_y = position
        if use_offset:
            self.position = (point_x + self.offset.x, point_y + self.offset.y)
        else:
            self.position = (point_x, point_y)

    def check_collide(self, position: tuple[int, int]) -> bool:
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
