from config import *
from gamedata import GameUnit, Player, GameMap, GameData, GameState, GameSettings
from geometry.collision import LineWithCollision
from models.game_model import GameModel
from models.profile import ModelProfile, ModelData
from basic_data.dc import GameParams, PlayerProfile
from basic_data.enums import GAME_SETTINGS_MODE
from basic_data.source import BLUE

player_profile1 = PlayerProfile('Neash')

index1 = ModelProfile(base_diameter=0.5, passable=True)
index2 = ModelProfile(base_diameter=1.5, passable=False)
models = [ModelData(index1) for _ in range(5)]
data2 = ModelData(index2)
unit_models = [GameModel(index1, data=ModelData(index1), position=(4, x)) for x in range(4, 14, 3)]
model2 = GameModel(index2, data=data2, position=(7.625, 6.125))

test_map = GameMap(size=(26, 22), terrain=[])


unit1 = GameUnit(unit_models)
unit2 = GameUnit([model2])

player1 = Player(player_profile=player_profile1, team=1, units=[unit1, unit2])
state = GameState()
state.player_act = player1
settings = GameSettings(GAME_SETTINGS_MODE.SINGLE)
gamedata = GameData(test_map, [player1], state, settings)
params = GameParams(FPS=FPS, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT, SCALE=SCALE)

