import pygame

from config import *
from dc import GameParams
from gamedata import GameData
from main import GameLoop

params = GameParams(FPS=FPS, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)
game = GameData()
game_loop = GameLoop(game_params=params, game_data=game)

game_loop.run()


pygame.quit()
