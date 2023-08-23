import pygame

from actions import Action, DragData
from geometry.base import BaseObject
from graphics.camera import GameCamera
from config import ZOOM_TOP_SPEED
from gamedata import GameData
from basic_data.source import *
from basic_data.dc import GameParams, ControlEvent, PlayerProfile
from basic_data.enums import ActionTypes, ControlEventTypes, MODE_NAMES, GAME_SETTINGS_MODE, GAME_STATE_NAMES, \
    BATTLE_PHASE_NAMES
from logic.collision.collision import CollisionMixin
from logic.event_checker import EventChecker
from graphics.draw import DrawingMaker
from interface import GameInterface
from logic.handlers import Handlers
from logic.collision.logic import GameLogic
from utils import to_screen_scale

clock = pygame.time.Clock()
running = True


class GameLoop:
    def __init__(self, player_profile: PlayerProfile, game_params: GameParams, gamedata: GameData):
        self.player_profile = player_profile
        self.params = game_params
        self.event_checker = EventChecker(self)
        self.graphics = DrawingMaker(self)
        self.logic = GameLogic(self)
        self.interface = GameInterface(self)
        self.camera: GameCamera | None = None
        self.gamedata = gamedata
        self.mode: MODE_NAMES = MODE_NAMES.MENU
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((game_params.SCREEN_WIDTH, game_params.SCREEN_HEIGHT))
        pygame.display.set_caption("Game")
        self.dragged_obj: CollisionMixin | None = None
        self.current_action: Action | None = None
        self.actions = []

        self._set_first_camera()
        self.handlers = Handlers(self)

    @property
    def player_act(self):
        return self.gamedata.player_act

    def _set_first_camera(self):
        if self.gamedata.settings.mode == GAME_SETTINGS_MODE.SINGLE:
            self.camera = self.gamedata.players[0].camera


    def run(self):
        while self.running:
            game_handler = self.choose_handler()
            camera_handler = self.handlers.camera
            for event in pygame.event.get():
                control_event = self.event_checker.check(event)
                camera_handler.handle(control_event)
                game_handler.handle(control_event)

                if control_event.type == ControlEventTypes.MOUSE_SEC_UP:
                    self.handle_second_mouse_up(control_event)

                    ##########

                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(DARK)
            self.graphics.draw_all(self.camera)
            pygame.display.flip()
            clock.tick(self.params.FPS)


    def check_mouse_inside(self, pos):
        x, y = pos
        return 0 < x < self.params.SCREEN_WIDTH and 0 < y < self.params.SCREEN_HEIGHT






    def handle_middle_mouse_down(self, event):
        if not self.current_action:
            if event.keys[pygame.K_SPACE] and not event.keys[pygame.K_LCTRL]:
                screen_pos = to_screen_scale(event.pos, self.camera.scale, *self.camera.pos, self.camera.angle)
                self.camera.rotate_zero = screen_pos[0]
                self.camera.rotate_anchor = screen_pos
                self.current_action = Action(ActionTypes.ROTATING_CAMERA)

            else:
                screen_pos = to_screen_scale(event.pos, self.camera.scale, *self.camera.pos, self.camera.angle)
                self.camera.drag_anchor = screen_pos
                self.current_action = Action(ActionTypes.DRAGGING_CAMERA, None)


    def handle_middle_mouse_up(self, event):
        if self.current_action:
            self.current_action.complete = True
            self.actions.append(self.current_action)
            self.current_action = None
            self.dragged_obj = None


    def handle_second_mouse_up(self, control_event):
        # TODO: Open some menu from self.interface.elements if it might be open
        pass



    def choose_handler(self):
        state = self.gamedata.game_state
        if state.name == GAME_STATE_NAMES.BATTLE:
            if state.battle_state.name == BATTLE_PHASE_NAMES.COMMAND:
                return self.handlers.command
            if state.battle_state.name == BATTLE_PHASE_NAMES.MOVE:
                return self.handlers.move
            if state.battle_state.name == BATTLE_PHASE_NAMES.SHOOT:
                return self.handlers.shoot
            if state.battle_state.name == BATTLE_PHASE_NAMES.CHARGE:
                return self.handlers.charge
            if state.battle_state.name == BATTLE_PHASE_NAMES.FIGHT:
                return self.handlers.fight
        if state.name == GAME_STATE_NAMES.INITIAL:
            return self.handlers.initial
