from typing import TYPE_CHECKING

import pygame
from pygame.event import Event

from basic_data.dc import ControlEvent
from basic_data.enums import ControlEventTypes
from utils import to_real_scale

if TYPE_CHECKING:
    from main import GameLoop


class EventChecker:
    def __init__(self, loop: 'GameLoop'):
        self.loop = loop
        self.MOUSE_EVENT_TYPES = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]

    def check(self, event: Event) -> ControlEvent:
        scale = self.loop.camera.scale
        pressed_keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        real_event_pos = (0, 0)
        event_type = ControlEventTypes.UNDEFINED
        event_data = None
        mouse_motion = False
        if event.type in self.MOUSE_EVENT_TYPES:
            real_event_pos = to_real_scale(event.pos, scale, *self.loop.camera.pos, self.loop.camera.angle)
        if event.type == pygame.MOUSEWHEEL:
            event_type = ControlEventTypes.SCROLL
            event_data = event.y

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                event_type = ControlEventTypes.MOUSE_MAIN_DOWN
            if event.button == 2:
                event_type = ControlEventTypes.MOUSE_MIDDLE_DOWN
            if event.button == 3:
                event_type = ControlEventTypes.MOUSE_SEC_DOWN
            if event.button == 6:
                event_type = ControlEventTypes.MOUSE_BACK_DOWN
            if event.button == 7:
                event_type = ControlEventTypes.MOUSE_FORTH_DOWN
        if event.type == pygame.MOUSEMOTION:
            mouse_motion = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                event_type = ControlEventTypes.MOUSE_MAIN_UP
            if event.button == 2:
                event_type = ControlEventTypes.MOUSE_MIDDLE_UP
            if event.button == 3:
                event_type = ControlEventTypes.MOUSE_SEC_UP
            if event.button == 6:
                event_type = ControlEventTypes.MOUSE_BACK_UP
            if event.button == 7:
                event_type = ControlEventTypes.MOUSE_FORTH_UP
        return ControlEvent(
            real_event_pos,
            type=event_type,
            data=event_data,
            keys=pressed_keys,
            mouse_pos=mouse_pos,
            mouse_motion=mouse_motion
        )


    def _check_pressed_keys(self, event):
        pass
