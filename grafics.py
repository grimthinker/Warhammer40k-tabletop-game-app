from typing import TYPE_CHECKING

import pygame

from geometry import Circle, Line
from utils import to_screen_scale

if TYPE_CHECKING:
    from main import GameLoop


class DrawingMaker:
    def __init__(self, loop: 'GameLoop'):
        self.loop = loop


    def draw(self, obj):
        screen = self.loop.screen
        scale = self.loop.camera.scale
        camera = self.loop.camera
        if isinstance(obj, Circle):
            size = obj.radius * scale
            position = to_screen_scale(obj.position, scale, *camera.pos)
            pygame.draw.circle(screen, obj.color, position, size, obj.line_wide)

        if isinstance(obj, Line):
            start = to_screen_scale(obj.start, scale, *camera.pos)
            end = to_screen_scale(obj.end, scale, *camera.pos)
            pygame.draw.line(
                screen,
                obj.color,
                start,
                end,
                obj.line_wide
            )

    def draw_all(self):
        for obj in self.loop.game_data.game_objects:
            self.draw(obj)

