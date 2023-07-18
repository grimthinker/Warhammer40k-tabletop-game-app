from typing import TYPE_CHECKING

from config import SCALE_MOVE_UP, SCALE_MOVE_DOWN, ZOOM_SPEED
from dc import ControlEvent
from utils import to_real_scale, to_screen_scale

if TYPE_CHECKING:
    from main import GameLoop


class GameCamera:
    def __init__(
            self,
            loop: 'GameLoop',
            scale: float = 40,
            pos: tuple[float, float] = (-10, -10),
            position_z: int = 0
    ):
        self.loop = loop
        self.scale = scale
        self.pos = pos
        self.position_z = position_z

        self.anchor: tuple[float, float] | None = None

    def zoom(self, event: ControlEvent, speed_mult: float = ZOOM_SPEED):

        center_pos = event.mouse_pos
        # old center real pos
        cx, cy = to_real_scale(center_pos, self.scale, *self.pos)
        if event.data == 1:
            self.scale *= (SCALE_MOVE_UP * speed_mult)
        elif event.data == -1:
            self.scale *= (SCALE_MOVE_DOWN / speed_mult)
        # new offset real pos
        nox, noy = to_real_scale(self.pos, self.scale, *self.pos)
        # new center real pos
        ncx, ncy = to_real_scale(center_pos, self.scale, *self.pos)
        dx, dy = ncx - nox, ncy - noy
        # required offset real pos
        rox, roy = cx - dx, cy - dy
        self.pos = to_screen_scale((rox, roy), self.scale, *self.pos)

    def drag(self, new_pos):
        ox, oy = self.anchor
        nx, ny = new_pos
        dx, dy = nx - ox, ny - oy
        x, y = self.pos
        self.pos = x - dx, y - dy
        self.anchor = new_pos






