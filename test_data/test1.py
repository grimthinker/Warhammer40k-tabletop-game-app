from config import *
from gamedata import GameUnit, Player, GameMap, GameData, GameState, GameSettings
from geometry.collision import LineWithCollision
from logic.classes import DInt
from logic.utils import calculate_damage_chance
from models.game_model import GameModel
from models.profile import ModelProfile, ModelData, RangedWeaponData, RangedWeapon
from basic_data.dc import GameParams, PlayerProfile
from basic_data.enums import GAME_SETTINGS_MODE, GAME_STATE_NAMES, BATTLE_PHASE_NAMES
from basic_data.source import BLUE

player_profile1 = PlayerProfile('Neash')

index1 = ModelProfile(base_diameter=0.5, passable=True, T=14, Sv=2, InvSv=None)
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
state.name = GAME_STATE_NAMES.BATTLE
state.battle_state.name = BATTLE_PHASE_NAMES.MOVE
state.player_act = player1
settings = GameSettings(GAME_SETTINGS_MODE.SINGLE)
gamedata = GameData(test_map, [player1], state, settings)
params = GameParams(FPS=FPS, SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT, SCALE=SCALE)


weapon = RangedWeapon(A=8, S=9, AP=-3, D=DInt(6, 0), BS=2)

# calculate_damage_chance(weapon, index1)