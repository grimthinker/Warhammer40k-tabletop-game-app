from typing import TYPE_CHECKING

import pygame

from geometry.base import Circle, Line
from utils import to_screen_scale

if TYPE_CHECKING:
    from main import GameLoop


class DrawingMaker:
    def __init__(self, loop: 'GameLoop'):
        self.loop = loop


    def draw(self, obj, camera):
        screen = self.loop.screen
        scale = camera.scale
        if isinstance(obj, Circle):

            size = obj.radius * scale
            position = to_screen_scale(obj.position, scale, *camera.pos, camera.angle)
            pygame.draw.circle(screen, obj.color, position, size, obj.line_wide)

        if isinstance(obj, Line):
            start = to_screen_scale(obj.start, scale, *camera.pos, camera.angle)
            end = to_screen_scale(obj.end, scale, *camera.pos, camera.angle)
            pygame.draw.line(
                screen,
                obj.color,
                start,
                end,
                obj.line_wide
            )

    def draw_all(self, camera):
        for obj in self.loop.gamedata.objects:
            self.draw(obj, camera)

        for element in self.loop.interface.elements.all:
            self.draw(element, camera)

