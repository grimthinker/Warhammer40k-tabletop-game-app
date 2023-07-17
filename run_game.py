import pygame

from config import *
from dc import GameParams
from gamedata import GameData
from main import GameLoop

params = GameParams(FPS=FPS, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT, SCALE=SCALE)
game = GameData(size_x=30, size_y=20)
game_loop = GameLoop(game_params=params, game_data=game)

game_loop.run()


pygame.quit()
