from logic.handlers.base import BaseHandler

import pygame

from actions import Action
from basic_data.enums import ControlEventTypes, ActionTypes
from config import ZOOM_TOP_SPEED
from utils import to_screen_scale


class CameraHandler(BaseHandler):
    def __init__(self, game_loop):
        super(CameraHandler, self).__init__(game_loop)


    def handle(self, event):
        if event.type == ControlEventTypes.MOUSE_MIDDLE_DOWN:
            self.handle_middle_mouse_down(event)

        if event.mouse_motion:
            self.handle_mouse_motion(event)

        if event.type == ControlEventTypes.MOUSE_MIDDLE_UP:
            self.handle_middle_mouse_up(event)

        if event.type == ControlEventTypes.SCROLL:
            self.handle_scroll(event)



    def handle_middle_mouse_down(self, event):
        if not self.current_action:
            if event.keys[pygame.K_SPACE] and not event.keys[pygame.K_LCTRL]:
                screen_pos = to_screen_scale(
                    event.pos,
                    self.loop.camera.scale,
                    *self.loop.camera.pos,
                    self.loop.camera.angle
                )
                self.loop.camera.rotate_zero = screen_pos[0]
                self.loop.camera.rotate_anchor = screen_pos
                self.current_action = Action(ActionTypes.ROTATING_CAMERA)

            else:
                screen_pos = to_screen_scale(
                    event.pos,
                    self.loop.camera.scale,
                    *self.loop.camera.pos,
                    self.loop.camera.angle
                )
                self.loop.camera.drag_anchor = screen_pos
                self.current_action = Action(ActionTypes.DRAGGING_CAMERA, None)


    def handle_middle_mouse_up(self, event):
        if self.current_action:
            self.current_action.complete = True
            self.loop.actions.append(self.current_action)
            self.current_action = None
            self.dragged_obj = None


    def handle_mouse_motion(self, event):
        new_screen_pos = to_screen_scale(event.pos, self.loop.camera.scale, *self.loop.camera.pos, self.loop.camera.angle)
        if self.loop.check_mouse_inside(new_screen_pos) and self.current_action:
            if self.current_action.type == ActionTypes.DRAGGING_CAMERA:
                self.loop.camera.drag(new_screen_pos)
            elif self.current_action.type == ActionTypes.ROTATING_CAMERA:
                self.loop.camera.rotate(event)


    def handle_scroll(self, event):
        if event.keys[pygame.K_LSHIFT] and not event.keys[pygame.K_LCTRL]:
            self.loop.camera.zoom(event, speed_mult=ZOOM_TOP_SPEED)

        if not event.keys[pygame.K_LSHIFT] and not event.keys[pygame.K_LCTRL]:
            self.loop.camera.zoom(event)
