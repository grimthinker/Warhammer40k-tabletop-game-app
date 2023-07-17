from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameLoop


class GameCamera:
    def __init__(self, loop: 'GameLoop', scale: float = 20, offset_x: float = 10, offset_y: float = 10):
        self.loop = loop
        self.scale = scale
        self.offset_x = offset_x
        self.offset_y = offset_y
