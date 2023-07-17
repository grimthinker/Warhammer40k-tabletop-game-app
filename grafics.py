from typing import TYPE_CHECKING

import pygame

from geometry import Circle, Line

if TYPE_CHECKING:
    from main import GameLoop


class DrawingMaker:
    def __init__(self, loop: 'GameLoop'):
        self.loop = loop


    def draw(self, obj):
        screen = self.loop.screen
        scale = self.loop.scale
        camera = self.loop.camera
        if isinstance(obj, Circle):
            size = obj.radius * scale
            x, y = obj.position
            position = [scale * x + camera.offset_x, scale * y + camera.offset_y]
            pygame.draw.circle(screen, obj.color, position, size, obj.line_wide)

        if isinstance(obj, Line):
            x0, y0 = obj.start
            x1, y1 = obj.end
            start = [scale * x0 + camera.offset_x, scale * y0 + camera.offset_y]
            end = [scale * x1 + camera.offset_x, scale * y1 + camera.offset_y]
            pygame.draw.line(
                screen,
                obj.color,
                start,
                end,
                obj.line_wide
            )

