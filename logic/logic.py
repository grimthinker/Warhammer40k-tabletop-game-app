from typing import TYPE_CHECKING

from gamedata import GameObject
from utils import distance_w

if TYPE_CHECKING:
    from main import GameLoop


class GameLogic:
    def __init__(self, loop: 'GameLoop'):
        self.loop = loop
        self.graphics = self.loop.graphics


    def check_move_length(self, dragged_obj: GameObject) -> bool:
        if dragged_obj.model:
            move = dragged_obj.model.data.M
        else:
            return False
        if dragged_obj.dragging_line:
            length = dragged_obj.dragging_line.length
        else:
            return False
        return move >= length


    def find_collided(self, obj: GameObject):
        collided = []
        for another_obj in self.loop.game_data.game_objects:
            if another_obj == obj or another_obj == obj.dragging_line:
                continue
            collision, distance = obj.check_collision(another_obj)
            if collision:
                collided.append([another_obj, distance])
        return collided


    def set_with_available_move(self, dragged_obj: GameObject):
        available_pos = dragged_obj.correct_length_move()
        self.loop.dragged_obj.set_pos(available_pos, use_offset=False)
        self.loop.dragged_obj.dragging_line.set_pos(self.loop.dragged_obj.position)



    def set_with_noncollide_position(
            self,
            dragged_obj: GameObject,
            collided_object: GameObject,
            proposed_pos: tuple[float, float]
    ):
        """Сдвигает передвигаемый объект ближе к изначальной точке так, чтобы не было пересечения с collided_object"""
        dragged_obj.set_with_noncollide_position(collided_object, proposed_pos)



    def set_dragged_obj_position(self, pos):
        self.loop.dragged_obj.set_pos(pos, use_offset=True)
        self.loop.dragged_obj.dragging_line.set_pos(self.loop.dragged_obj.position)



