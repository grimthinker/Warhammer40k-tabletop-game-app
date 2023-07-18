import math

from geometry.base import BaseObject, Line, Circle, Rectangle
from utils import find_correction_circle, find_angle, length, distance_w, check_intersection


class CollisionMixin(BaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_collision(self, another_obj: 'BaseObject'):
        current_distance = 0
        limit = math.inf
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

    def correct_length_move(self, correct_length: float | None = None) -> tuple[float, float]:
        correct_length = correct_length if correct_length else self.model.profile.M
        length = self.dragging_line.length
        m = correct_length / (length + 0.00001)
        start_x, start_y = self.dragging_line.position
        end_x, end_y = self.dragging_line.end
        d_x = end_x - start_x
        d_y = end_y - start_y
        return ((start_x + d_x * m), (start_y + d_y * m))

    def set_with_noncollide_position(
            self,
            proposed_pos: tuple[float, float],
            objects: list,
            correct_length: int | None = None,
        ):

        correct_length = correct_length if correct_length else self.model.profile.M
        correction = 0
        collided = self.find_collided(objects)
        old_correct_up = True
        correct_up = True
        for _ in range(250):
            for collided_object, distance in collided:

                if not isinstance(self, CollisionMixin) or not isinstance(collided_object, CollisionMixin):
                    continue

                collided = self.find_collided(objects)
                collision, distance = self.check_collision(collided_object)
                if collision or collided:
                    try:
                        if isinstance(self, Circle) and isinstance(collided_object, Circle):
                            error = self.radius + collided_object.radius - distance
                            correction = error * 0.1 * ((self.radius + collided_object.radius) / collided_object.radius)

                        if isinstance(self, Circle) and isinstance(collided_object, Line):
                            error = self.radius - distance
                            correction = error * 0.1
                        another_collision = self.check_another_collision(collided_object, collided)
                        correct_up_possible = self.check_correct_up_possible(collided_object, correct_length)
                        if not correct_up_possible or another_collision:
                            if correct_up:
                                correct_up = False
                        if correct_up:
                            correct_length_move = self.dragging_line.length + correction
                        else:
                            correct_length_move = self.dragging_line.length - correction
                        available_pos = self.correct_length_move(correct_length_move)
                        self.set_pos(available_pos, use_offset=False)
                        self.dragging_line.set_pos(self.position)
                    except ValueError as e:  # Occasional math errors when trying to correct position. Maybe just pass them?
                        print(e)
                else:
                    break
        return correct_up

    def find_collided(self, objects: list):
        collided = []
        for another_obj in objects:
            if another_obj == self or another_obj == self.dragging_line:
                continue
            collision, distance = self.check_collision(another_obj)
            if collision:
                collided.append([another_obj, distance])
        return collided


    def check_correct_up_possible(self, collided_object, correct_length: int | None = None):
        proposed_move = self.dragging_line.length
        if isinstance(self, Circle) and isinstance(collided_object, Circle):
            _line = Line(position=0, start=self.dragging_line.start, end=collided_object.position)
            _cos = math.cos(find_angle(self.dragging_line, _line))
            _x = _line.length * _cos
            correct_length = correct_length if correct_length else self.model.profile.M
            if _x < proposed_move < correct_length:
                return True
            else:
                return False
        if isinstance(self, Circle) and isinstance(collided_object, Line):
            _intersection = check_intersection(self.dragging_line, collided_object)
            if proposed_move < correct_length and _intersection:
                return True
            else:
                return False


    def check_another_collision(self, collided_object, objects: list):
        for obj, _ in objects:
            if collided_object != obj:
                return True
        return False


    def calculate_correction(self, correct_up):
        pass

