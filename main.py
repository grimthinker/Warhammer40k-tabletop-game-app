import pygame

from actions import Action, DragData
from camera import GameCamera
from data import *
from dc import GameParams
from enums import ActionTypes
from gamedata import GameData, GameObject
from grafics import DrawingMaker
from logic import GameLogic

clock = pygame.time.Clock()
running = True

MOUSE_EVENT_TYPES = [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION]


class GameLoop:
    def __init__(self, game_params: GameParams, game_data: GameData):
        self.params = game_params
        self.graphics = DrawingMaker(self)
        self.logic = GameLogic(self)
        self.camera = GameCamera(self)
        self.scale = self.camera.scale
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
                if event.type in MOUSE_EVENT_TYPES:
                    x, y = event.pos
                    real_event_pos = [(x - self.camera.offset_x) / self.scale, (y - self.camera.offset_y) / self.scale]
                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.current_action:
                    for obj in self.game_data.game_objects:
                        if obj.check_point(real_event_pos) and obj.draggable:
                            obj.dragging = True
                            self.dragged_obj: GameObject = obj
                            data = DragData(obj, start_pos=obj.position, start_pos_z=obj.position_z)
                            self.current_action = Action(type=ActionTypes.DRAG, data=data)
                            self.game_data.game_objects.append(obj.make_dragging_line(GREEN, obj.position))
                            break

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    if self.dragged_obj:
                        self.dragged_obj.dragging = False
                        self.game_data.game_objects.remove(self.dragged_obj.dragging_line)
                        self.current_action.data.end_pos = self.dragged_obj.position
                        self.current_action.data.end_pos_z = self.dragged_obj.position_z
                        self.current_action.complete = True
                        self.actions.append(self.current_action)
                        self.current_action = None
                        self.dragged_obj = None

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragged_obj and self.check_mouse_inside(event.pos):
                        self.logic.set_dragged_obj_position(real_event_pos)
                        if not self.logic.check_move_length(self.dragged_obj):
                            self.logic.set_with_available_move(self.dragged_obj)

                        for _ in range(180):
                            collided = self.logic.find_collided(self.dragged_obj)
                            for collided_object, distance in collided:
                                self.logic.set_with_noncollide_position(self.dragged_obj, collided_object, distance)


            self.screen.fill(DARK)
            for obj in self.game_data.game_objects:
                self.graphics.draw(obj)

            pygame.display.flip()
            clock.tick(self.params.FPS)

    def check_mouse_inside(self, pos):
        x, y = pos
        return 0 < x < self.params.SCREEN_WIDTH and 0 < y < self.params.SCREEN_HEIGHT


