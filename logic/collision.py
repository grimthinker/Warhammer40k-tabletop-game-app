import math

import pygame

from basic_data.source import ORANGE
from config import COLLISION_CHECKS_NUMBER
from geometry.base import BaseObject, Line, Circle, Rectangle
from basic_data.enums import COLLISION_TYPE
from utils import find_angle, length, distance_w, check_intersection, ccw, segments_intersect


class CollisionMixin(BaseObject):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def check_collision(self, another_obj: 'BaseObject'):
        current_distance = 0
        limit = math.inf
        if isinstance(another_obj, Line) and isinstance(self, Line):
            return check_intersection(another_obj, self), 0, another_obj
        if isinstance(another_obj, Line) and isinstance(self, Circle):
            limit = self.radius
            current_distance = distance_w(another_obj.position, another_obj.end, self.position)
        if isinstance(another_obj, Circle) and isinstance(self, Line):
            limit = another_obj.radius
            current_distance = distance_w(self.position, self.end, another_obj.position)
        if isinstance(another_obj, Circle) and isinstance(self, Circle):
            limit = another_obj.radius + self.radius
            current_distance = length(another_obj.position, self.position)
        if isinstance(another_obj, Rectangle) and isinstance(self, Circle):
            for line in another_obj.lines:
                pass
        return current_distance <= limit, current_distance, another_obj

    def correct_length_move(self, correct_length: float | None = None) -> tuple[float, float]:
        correct_length = correct_length if correct_length else self.model.profile.M
        length = self.last_dragging_line.length
        m = correct_length / (length + 0.000001)
        start_x, start_y = self.last_dragging_line.position
        end_x, end_y = self.last_dragging_line.end
        d_x = end_x - start_x
        d_y = end_y - start_y
        return ((start_x + d_x * m), (start_y + d_y * m))


    def noncollide_pos_simplest(self, req_pos, objects, offset=None):
        self.set_pos_all(req_pos, offset)
        req_move = self.last_dragging_line.length
        curr_move = req_move
        if curr_move >= self.model.data.M:
            self.set_corrected_pos_all(self.model.data.M)

        min_not_passing_move = self.find_not_passing_move(objects, curr_move, down=True)
        max_not_passing_move = self.find_not_passing_move(objects, 0, down=False)
        max_available_move = min(self.model.data.M, max_not_passing_move)
        self.set_corrected_pos_all(min_not_passing_move)
        curr_move = self.last_dragging_line.length

        max_not_colliding_move = self.find_not_colliding_move(objects, curr_move, req_move, max_available_move, down=False)
        curr_move = self.last_dragging_line.length
        min_not_colliding_move = self.find_not_colliding_move(objects, curr_move, req_move, max_available_move, down=True)



    def set_pos_all(self, position: tuple[float, float], use_offset=False):
        self.set_pos(position, use_offset=use_offset)
        self.last_dragging_line.set_pos(self.position)
        self.last_move_line.set_pos(self.position)
        self.correct_move_borders()

    def set_corrected_pos_all(self, lenght):
        available_pos = self.correct_length_move(lenght)
        self.set_pos(available_pos, use_offset=False)
        self.last_dragging_line.set_pos(self.position)
        self.last_move_line.set_pos(self.position)
        self.correct_move_borders()

    def find_passed(self, objects: list['CollisionMixin']):
        passed = []
        border1, border2 = self.last_move_borders
        for another_obj in objects:
            if (
                another_obj == self or
                another_obj in [border1.moving_object] or
                another_obj in [border1, border2] or
                another_obj.passable
            ): continue
            for border in border1, border2:
                collision, _, collided_obj = border.check_collision(another_obj)
                if collision and collided_obj not in passed:
                    passed.append(collided_obj)
        return passed

    def find_collided(self, objects: list['CollisionMixin']):
        collided = []
        for another_obj in objects:
            if (
                another_obj == self or
                another_obj in self.last_move_borders or
                another_obj in self.dragging_lines or
                another_obj in self.move_lines
            ): continue
            if another_obj.can_be_stood_on: continue
            collision, distance, collided_obj = self.check_collision(another_obj)
            if collision:
                collided.append([another_obj, distance])
        return collided


    def check_correct_up_possible(self, collided_object, required_move, proposed_move, correct_length):
        if isinstance(self, Circle) and isinstance(collided_object, Circle):
            _line = Line(position=0, start=self.last_dragging_line.position, end=collided_object.position)
            _cos = math.cos(find_angle(self.last_dragging_line, _line))
            _x = _line.length * _cos
            if _x <= required_move and proposed_move <= correct_length:
                return True
            else:
                return False
        if isinstance(self, Circle) and isinstance(collided_object, Line):
            _intersection = check_intersection(self.last_dragging_line, collided_object)
            if proposed_move < correct_length and _intersection:
                return True
            else:
                return False

    def find_not_passing_move(self, objects, current_move, down):
        def _down(move):
            return move - (move * 0.011 + 0.009)

        def _up(move):
            return move + (move * 0.011 + 0.009)

        def _break_mdown(passed):
            return not passed

        def _break_mup(passed):
            return passed or proposed_move > self.model.data.M

        f = _down if down else _up
        _break = _break_mdown if down else _break_mup
        move = current_move
        for _ in range(COLLISION_CHECKS_NUMBER):
            passed = self.find_passed(objects)
            proposed_move = f(move)
            if _break(passed):
                break
            self.set_corrected_pos_all(proposed_move)
            move = self.last_dragging_line.length
        return self.last_dragging_line.length


    def find_not_colliding_move(self, objects, current_move, required_move, max_available_move, down):
        def _down(move):
            return move - (move * 0.011 + 0.009)

        def _up(move):
            return move + (move * 0.011 + 0.009)

        def _break_mdown(collided):
            return not collided

        def _break_mup(collided):
            check_correct_up_possible = all(
                [self.check_correct_up_possible(
                    obj, required_move, proposed_move, max_available_move
                ) for obj, distance in collided]
            )
            return not check_correct_up_possible or not collided

        f = _down if down else _up
        _break = _break_mdown if down else _break_mup
        move = current_move
        for _ in range(COLLISION_CHECKS_NUMBER):
            collided = self.find_collided(objects)
            proposed_move = f(move)

            if _break(collided):
                break
            self.set_corrected_pos_all(proposed_move)
            move = self.last_dragging_line.length
        return self.last_dragging_line.length

