import math

from geometry.base import Line, Circle, Rectangle
from logic.collision import CollisionMixin
from utils import ang


class LineWithCollision(Line, CollisionMixin):
    pass


class CircleWithCollision(Circle, CollisionMixin):
    def make_move_borders(self, color: tuple[int, int, int], position: tuple[int, int]):
        a = ang(self.last_move_line.vector, (1, 0), full=True)
        r = self.radius
        x0, y0 = self.position
        position1 = x0 + math.sin(a) * r, y0 + math.cos(a) * r
        position2 = x0 - math.sin(a) * r, y0 - math.cos(a) * r
        border1 = LineWithCollision(color=color, position=position1, start=position1, end=position1, moving_object=self)
        border2 = LineWithCollision(color=color, position=position2, start=position2, end=position2, moving_object=self)
        self.move_borders.append((border1, border2))
        return border1, border2


class RectangleWithCollision(Rectangle, CollisionMixin):
    pass
