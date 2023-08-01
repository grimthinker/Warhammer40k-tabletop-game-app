from config import *
from gamedata import GameUnit, Player, GameMap, GameData, GameState, GameSettings
from geometry.collision import LineWithCollision
from models.game_model import GameModel
from models.profile import ModelProfile, ModelData
from basic_data.dc import GameParams, PlayerProfile
from basic_data.enums import GAME_SETTINGS_MODE
from basic_data.source import BLUE

player_profile1 = PlayerProfile('Neash')

index1 = ModelProfile(base_diameter=0.5)
index2 = ModelProfile(base_diameter=1.5)
data1 = ModelData()
data2 = ModelData()
model = GameModel(index1, data=data1, position=(4, 4))
model2 = GameModel(index2, data=data2, position=(7.625, 6.125))

test_map = GameMap(size=(16, 12), terrain=[])

models = [model, model2]  # game models

unit1 = GameUnit(models)
unit2 = GameUnit([])

player1 = Player(player_profile=player_profile1, team=1, units=[unit1])
state = GameState()
state.player_act = player1
settings = GameSettings(GAME_SETTINGS_MODE.SINGLE)
gamedata = GameData(test_map, [player1], state, settings)
params = GameParams(FPS=FPS, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT, SCALE=SCALE)

