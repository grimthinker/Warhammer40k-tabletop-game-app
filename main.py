import pygame

from actions import Action, DragData
from data import *
from dc import GameParams
from enums import ActionTypes
from gamedata import GameData, GameObject
from utils import make_line

clock = pygame.time.Clock()
running = True

class GameLoop:
    def __init__(self, game_params: GameParams, game_data: GameData):
        self.SCREEN_WIDTH = game_params.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game_params.SCREEN_HEIGHT
        self.FPS = game_params.FPS
        self.BASE_SCALE = game_params.SCALE
        self.scale = game_params.SCALE
        self.game_data = game_data
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tracking System")

        self.dragged_obj: GameObject | None = None
        self.current_action: Action | None = None
        self.actions = []


    def run(self):
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.current_action:
                    for obj in self.game_data.game_objects:
                        if obj.check_collide(event.pos) and obj.draggable:
                            obj.dragging = True
                            self.dragged_obj = obj
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
                    if self.dragged_obj and self.dragged_obj.dragging:
                        self.dragged_obj.set_pos(event.pos, use_offset=True)
                        self.dragged_obj.dragging_line.set_pos(self.dragged_obj.position)
                        if self.dragged_obj.check_move(scale=self.scale):


            self.screen.fill(WHITE)
            for obj in self.game_data.game_objects:
                obj.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.FPS)

