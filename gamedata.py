from typing import TYPE_CHECKING

import pygame

from game_models import ModelProfile, ModelData, BaseModel
from data import RED, BLUE, BLACK
from geometry.base import BaseObject
from geometry.collision import LineWithCollision, CircleWithCollision

if TYPE_CHECKING:
    from dc import Offset, Position, GameParams

GameObject = BaseObject | LineWithCollision | CircleWithCollision

index = ModelProfile()
index2 = ModelProfile(base_diameter=3)
data = ModelData()
model = BaseModel(index, draggable=True, data=data)
model2 = BaseModel(index2, draggable=True, data=data)


test_data = [
    CircleWithCollision(color=RED, position=(4, 4), model=model),
    CircleWithCollision(color=RED, position=(7.625, 6.125), model=model2),
    LineWithCollision(color=BLUE, position=0, start=(3, 7), end=(7, 5))]


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
        top = LineWithCollision(color=BLACK, position=0, start=TL, end=TR)
        bottom = LineWithCollision(color=BLACK, position=0, start=BR, end=BL)
        left = LineWithCollision(color=BLACK, position=0, start=TL, end=BL)
        right = LineWithCollision(color=BLACK, position=0, start=BR, end=TR)
        self.game_objects.extend((top, bottom, left, right))
