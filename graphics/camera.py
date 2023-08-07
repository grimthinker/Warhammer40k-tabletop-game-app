from typing import TYPE_CHECKING

from config import SCALE_MOVE_UP, SCALE_MOVE_DOWN, ZOOM_SPEED, ROTATE_SPEED
from basic_data.dc import ControlEvent
from utils import to_real_scale, to_screen_scale

if TYPE_CHECKING:
    pass


class GameCamera:
    def __init__(
            self,
            scale: float = 40,
            pos: tuple[float, float] = (-10, -10),
            angle: float = 50,
            position_z: int = 0
    ):
        self.scale = scale
        self.pos = pos
        self.angle = angle
        self.position_z = position_z

        self.drag_anchor: tuple[float, float] | None = None
        self.rotate_zero: float | None = None
        self.rotate_anchor: tuple[float, float] | None = None


    def zoom(self, event: ControlEvent, speed_mult: float = ZOOM_SPEED):

        center_pos = event.mouse_pos
        # old center real pos
        cx, cy = to_real_scale(center_pos, self.scale, *self.pos, self.angle)
        if event.data == 1:
            self.scale *= (SCALE_MOVE_UP * speed_mult)
        elif event.data == -1:
            self.scale *= (SCALE_MOVE_DOWN / speed_mult)
        # new offset real pos
        nox, noy = to_real_scale(self.pos, self.scale, *self.pos, self.angle)
        # new center real pos
        ncx, ncy = to_real_scale(center_pos, self.scale, *self.pos, self.angle)
        dx, dy = ncx - nox, ncy - noy
        # required offset real pos
        rox, roy = cx - dx, cy - dy
        self.pos = to_screen_scale((rox, roy), self.scale, *self.pos, self.angle)

    def drag(self, new_pos):
        ox, oy = self.drag_anchor
        nx, ny = new_pos
        dx, dy = nx - ox, ny - oy
        x, y = self.pos
        self.pos = x - dx, y - dy
        self.drag_anchor = new_pos

    def rotate(self, event):
        cx, cy = to_real_scale(self.rotate_anchor, self.scale, *self.pos, self.angle)
        dx = (self.rotate_zero - event.mouse_pos[0]) * ROTATE_SPEED
        self.rotate_zero = event.mouse_pos[0]
        self.angle += dx
        nox, noy = to_real_scale(self.pos, self.scale, *self.pos, self.angle)
        # new center real pos
        ncx, ncy = to_real_scale(self.rotate_anchor, self.scale, *self.pos, self.angle)
        dx, dy = ncx - nox, ncy - noy
        # required offset real pos
        rox, roy = cx - dx, cy - dy
        self.pos = to_screen_scale((rox, roy), self.scale, *self.pos, self.angle)


