import pygame

from actions import Action, DragData
from camera import GameCamera
from config import ZOOM_TOP_SPEED
from data import *
from dc import GameParams, ControlEvent
from enums import ActionTypes, ControlEventTypes
from event_checker import EventChecker
from gamedata import GameData, GameObject
from grafics import DrawingMaker
from interface import GameInterface
from logic.logic import GameLogic
from utils import to_real_scale, to_screen_scale

clock = pygame.time.Clock()
running = True

MOUSE_EVENT_TYPES = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]


class GameLoop:
    def __init__(self, game_params: GameParams, game_data: GameData):
        self.params = game_params
        self.event_checker = EventChecker(self)
        self.graphics = DrawingMaker(self)
        self.logic = GameLogic(self)
        self.interface = GameInterface(self)
        self.camera = GameCamera(self)
        self.game_data = game_data
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((game_params.SCREEN_WIDTH, game_params.SCREEN_HEIGHT))
        pygame.display.set_caption("Tracking System")

        self.dragged_obj: GameObject | None = None
        self.current_action: Action | None = None
        self.actions = []

        self.game_data.create_borders()


    def run(self):
        while self.running:
            for event in pygame.event.get():

                real_event_pos = [0, 0]
                control_event = self.event_checker.check(event)
                if control_event.type == ControlEventTypes.SCROLL:
                    self.handle_scroll(control_event)

                if control_event.type == ControlEventTypes.MOUSE_MAIN_DOWN:
                    self.handle_main_mouse_down(control_event)

                if control_event.type == ControlEventTypes.MOUSE_MOTION:
                    self.handle_mouse_motion(control_event)

                if control_event.type == ControlEventTypes.MOUSE_MAIN_UP:
                    self.handle_main_mouse_up(control_event)

                if control_event.type == ControlEventTypes.MOUSE_MIDDLE_DOWN:
                    self.handle_middle_mouse_down(control_event)

                if control_event.type == ControlEventTypes.MOUSE_MIDDLE_UP:
                    self.handle_middle_mouse_up(control_event)



                if control_event.type == ControlEventTypes.MOUSE_SEC_UP:
                    self.handle_second_mouse_up(control_event)
                    ##########

                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(DARK)
            self.graphics.draw_all()
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
            for element in self.interface.elements:
                # TODO: interact with some interface element
                pass
            for obj in self.game_data.game_objects:
                if obj.check_point(event.pos) and obj.draggable:
                    # pygame.mouse.set_visible(False)
                    obj.dragging = True
                    self.dragged_obj: GameObject = obj
                    data = DragData(obj, start_pos=obj.position, start_pos_z=obj.position_z)
                    self.current_action = Action(ActionTypes.DRAGGING_MODEL, data)
                    self.game_data.game_objects.append(obj.make_dragging_line(GREEN, obj.position))
                    break
            else:
                pass


    def handle_main_mouse_up(self, event):
        if self.current_action:
            if self.current_action.type == ActionTypes.DRAGGING_MODEL:
                # pygame.mouse.set_visible(True)
                self.dragged_obj.dragging = False
                self.game_data.game_objects.remove(self.dragged_obj.dragging_line)
                self.current_action.data.end_pos = self.dragged_obj.position
                self.current_action.data.end_pos_z = self.dragged_obj.position_z
                self.current_action.complete = True
                self.actions.append(self.current_action)
                self.current_action = None
                self.dragged_obj = None


    def handle_mouse_motion(self, event: ControlEvent):
        new_screen_pos = to_screen_scale(event.pos, self.camera.scale, *self.camera.pos)
        if self.check_mouse_inside(new_screen_pos) and self.current_action:
            if self.current_action.type == ActionTypes.DRAGGING_MODEL:
                self.logic.set_dragged_obj_position(event.pos)
                if not self.logic.check_move_length(self.dragged_obj):
                    self.logic.set_with_available_move(self.dragged_obj)
                self.logic.set_with_noncollide_position(
                    self.dragged_obj,
                    event.pos,
                    self.game_data.game_objects,
                )

            elif self.current_action.type == ActionTypes.DRAGGING_CAMERA:
                self.camera.drag(new_screen_pos)


    def handle_middle_mouse_down(self, event):
        if not self.current_action:
            screen_pos = to_screen_scale(event.pos, self.camera.scale, *self.camera.pos)
            self.camera.anchor = screen_pos
            data = DragData(self.camera, start_pos=screen_pos, start_pos_z=self.camera.position_z)
            self.current_action = Action(ActionTypes.DRAGGING_CAMERA, data)


    def handle_middle_mouse_up(self, event):
        if self.current_action and self.current_action.type == ActionTypes.DRAGGING_CAMERA:
            self.current_action.data.end_pos = self.camera.pos
            self.current_action.data.end_pos_z = self.camera.position_z
            self.current_action.complete = True
            self.actions.append(self.current_action)
            self.current_action = None
            self.dragged_obj = None


    def handle_second_mouse_up(self, control_event):
        # TODO: Open some menu from self.interface.elements if it might be open
        pass

