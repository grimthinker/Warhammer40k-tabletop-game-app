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
from logic.collision import CollisionMixin
from logic.event_checker import EventChecker
from graphics.draw import DrawingMaker
from interface import GameInterface
from logic.handlers import Handlers
from logic.logic import GameLogic
from utils import to_screen_scale

clock = pygame.time.Clock()
running = True


class GameLoop:
    def __init__(self, player_profile: PlayerProfile, game_params: GameParams, gamedata: GameData):
        self.player_profile = player_profile
        self.params = game_params
        self.event_checker = EventChecker(self)
        self.handlers = Handlers(self)
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

                if control_event.mouse_motion:
                    self.handle_mouse_motion(control_event)

                if control_event.type == ControlEventTypes.MOUSE_MAIN_DOWN:
                    self.handle_main_mouse_down(control_event)

                if control_event.type == ControlEventTypes.MOUSE_MAIN_UP:
                    self.handle_main_mouse_up(control_event)



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


    def handle_scroll(self, event: ControlEvent):
        if event.keys[pygame.K_LSHIFT] and not event.keys[pygame.K_LCTRL]:
            self.camera.zoom(event, speed_mult=ZOOM_TOP_SPEED)

        if not event.keys[pygame.K_LSHIFT] and not event.keys[pygame.K_LCTRL]:
            self.camera.zoom(event)


    def handle_main_mouse_down(self, event: ControlEvent):
        if not self.current_action:
            for element in self.interface.elements.interactive:
                # TODO: interact with some interface element
                pass
            for obj in self.gamedata.objects:
                if obj.check_point(event.pos) and self.check_draggable(obj):
                    # pygame.mouse.set_visible(False)
                    self.set_dragging_obj(obj)
                    data = DragData(obj, start_pos=obj.position, start_pos_z=obj.position_z)
                    self.current_action = Action(ActionTypes.DRAGGING_MODEL, data)
                    obj.make_dragging_line(GREEN, obj.position)
                    obj.make_move_line(GREEN, obj.position)
                    self.interface.elements.temp.extend(obj.make_move_borders(GREEN, obj.position))
                    self.interface.elements.temp.append(obj.make_footprint(GREEN))
                    break
            else:
                pass


    def handle_main_mouse_up(self, event):
        if self.current_action:
            if self.current_action.type == ActionTypes.DRAGGING_MODEL:
                # pygame.mouse.set_visible(True)
                self.dragged_obj.dragging = False
                self.interface.elements.temp.remove(self.dragged_obj.last_footprint)
                for border in self.dragged_obj.last_move_borders:
                    self.interface.elements.temp.remove(border)
                self.current_action.data.end_pos = self.dragged_obj.position
                self.current_action.data.end_pos_z = self.dragged_obj.position_z
                self.current_action.complete = True
                self.actions.append(self.current_action)
                self.current_action = None
                self.dragged_obj = None


    def handle_mouse_motion(self, event: ControlEvent):
        new_screen_pos = to_screen_scale(event.pos, self.camera.scale, *self.camera.pos, self.camera.angle)
        if self.check_mouse_inside(new_screen_pos) and self.current_action:
            if self.current_action.type == ActionTypes.DRAGGING_MODEL:
                self.dragged_obj.noncollide_pos_simplest(
                    event.pos,
                    self.gamedata.objects,
                    True
                )



            elif self.current_action.type == ActionTypes.DRAGGING_CAMERA:
                self.camera.drag(new_screen_pos)
            elif self.current_action.type == ActionTypes.ROTATING_CAMERA:
                size = self.screen.get_size()
                rot_center = [size[0]/2, size[1]*5/6]
                self.camera.rotate(event)

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

    def check_draggable(self, obj: BaseObject):
        current_player = self.player_profile
        player_act = self.player_act.player_profile
        obj_owner = obj.owner.player_profile
        if current_player is player_act and obj_owner is current_player:
            return True
        return False

    def set_dragging_obj(self, obj):
        obj.dragging = True
        self.dragged_obj = obj

    def choose_handler(self):
        state = self.gamedata.game_state
        if state.name == GAME_STATE_NAMES.BATTLE:
            if state.battle_phase == BATTLE_PHASE_NAMES.COMMAND:
                return self.handlers.command
            if state.battle_phase == BATTLE_PHASE_NAMES.MOVE:
                return self.handlers.move
            if state.battle_phase == BATTLE_PHASE_NAMES.SHOOT:
                return self.handlers.shoot
            if state.battle_phase == BATTLE_PHASE_NAMES.CHARGE:
                return self.handlers.charge
            if state.battle_phase == BATTLE_PHASE_NAMES.FIGHT:
                return self.handlers.fight
        if state.name == GAME_STATE_NAMES.INITIAL:
            return self.handlers.initial
