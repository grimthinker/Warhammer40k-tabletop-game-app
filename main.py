import pygame

from data import *
from dc import GameParams
from gamedata import GameData, GameObject
from utils import make_line

clock = pygame.time.Clock()
running = True

class GameLoop:
    def __init__(self, game_params: GameParams, game_data: GameData):
        self.SCREEN_WIDTH = game_params.SCREEN_WIDTH
        self.SCREEN_HEIGHT = game_params.SCREEN_HEIGHT
        self.FPS = game_params.FPS
        self.game_data = game_data
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Tracking System")

        self.dragged_obj: GameObject | None = None


    def run(self):
        while self.running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for obj in self.game_data.game_objects:
                            if obj.check_collide(event.pos) and obj.draggable:
                                obj.dragging = True
                                self.dragged_obj = obj
                                self.game_data.game_objects.append(obj.make_dragging_line(GREEN, obj.position))
                                break

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if self.dragged_obj:
                            self.dragged_obj.dragging = False
                            self.game_data.game_objects.remove(self.dragged_obj.dragging_line)
                            self.dragged_obj = None

                elif event.type == pygame.MOUSEMOTION:
                    if self.dragged_obj and self.dragged_obj.dragging:
                        self.dragged_obj.set_pos(event.pos, use_offset=True)
                        self.dragged_obj.dragging_line.set_pos(self.dragged_obj.position)

            self.screen.fill(WHITE)
            for obj in self.game_data.game_objects:
                obj.draw(self.screen)

            pygame.display.flip()
            clock.tick(self.FPS)

