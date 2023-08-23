from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main import GameLoop


class GameLogic:
    def __init__(self, loop: 'GameLoop'):
        self.loop = loop
        self.graphics = self.loop.graphics


    def check_move_length(self, dragged_obj) -> bool:
        if dragged_obj.model:
            available_move = dragged_obj.model.data.M
        else:
            return False
        if dragged_obj.last_dragging_line:
            length = dragged_obj.last_dragging_line.length
        else:
            return False
        return available_move >= length


    def set_with_noncollide_position(
            self,
            dragged_obj,
            objects: list,
    ):
        """Сдвигает передвигаемый объект ближе к изначальной точке так, чтобы не было пересечения с collided_object"""
        return dragged_obj.noncollide_pos_simple(objects)






