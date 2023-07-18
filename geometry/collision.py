from geometry.base import Line, Circle, Rectangle
from logic.collision import CollisionMixin


class LineWithCollision(Line, CollisionMixin):
    pass


class CircleWithCollision(Circle, CollisionMixin):
    pass


class RectangleWithCollision(Rectangle, CollisionMixin):
    pass