from typing import TYPE_CHECKING

import pygame

from game_models import ModelProfile, ModelData
from geometry import Circle, BaseObject, BaseModel, Line
from data import RED, BLUE, BLACK

if TYPE_CHECKING:
    from dc import Offset, Position, GameParams

GameObject = BaseObject | Line | Circle

index = ModelProfile()
data = ModelData()
model = BaseModel(index, draggable=True, data=data)

test_data = [
    Circle(color=RED, position=(4, 4), model=model),
    Circle(color=RED, position=(2, 8), model=model),
    Line(color=BLUE, position=(3, 7), end=(7, 5))]


class GameData:
    def __init__(self, size_x: float, size_y: float):
        self.size_x = size_x
        self.size_y = size_y
        self.game_objects: list[GameObject] = test_data


    def create_borders(self):
        TL = (0, 0)
        TR = (0, self.size_y)
        BR = (self.size_x, self.size_y)
        BL = (self.size_x, 0)
        top = Line(color=BLACK, position=TL, end=TR)
        bottom = Line(color=BLACK, position=BR, end=BL)
        left = Line(color=BLACK, position=TL, end=BL)
        right = Line(color=BLACK, position=BR, end=TR)
        self.game_objects.extend((top, bottom, left, right))
