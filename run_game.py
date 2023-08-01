import pygame

from main import GameLoop
from test_data.test1 import*

game_loop = GameLoop(game_params=params, gamedata=gamedata, player_profile=player_profile1)

game_loop.run()
pygame.quit()
