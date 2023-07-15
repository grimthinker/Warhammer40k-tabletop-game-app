import pygame

from game_models import ModelProfile
from geometry import Circle, BaseObject, BaseModel, Line
from data import RED
from dc import Offset, Position


GameObject = BaseObject | Line | Circle

index = ModelProfile()
model = BaseModel(index, draggable=True)
test_data = [Circle(color=RED, position=(40, 40), radius=21, model=model)]

class GameData:
    def __init__(self):
        self.game_objects: list[GameObject] = test_data

