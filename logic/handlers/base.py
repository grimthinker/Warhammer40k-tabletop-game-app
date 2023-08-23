from typing import TYPE_CHECKING

import pygame

from actions import Action
from basic_data.enums import ControlEventTypes, ActionTypes
from config import ZOOM_TOP_SPEED
from utils import to_screen_scale

if TYPE_CHECKING:
    from main import GameLoop


class BaseHandler:
    def __init__(self, game_loop: 'GameLoop'):
        self.loop = game_loop
        self.camera = game_loop.camera
        self.current_action: Action | None = None
        self.actions = []

    @property
    def gamedata(self):
        return self.loop.gamedata

    @property
    def state(self):
        return self.loop.gamedata.game_state

    def handle(self, event):
        pass