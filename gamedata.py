from typing import TYPE_CHECKING

from basic_data.dc import PlayerProfile
from graphics.camera import GameCamera
from models.game_model import GameModel, TerrainModel
from basic_data.enums import GAME_STATE_NAMES, BATTLE_PHASE_NAMES, GAME_SETTINGS_MODE
from basic_data.source import WHITE
from geometry.collision import LineWithCollision

if TYPE_CHECKING:
    pass


class GameUnit:
    def __init__(self, models: list[GameModel]):
        self.models = models
        self.alife_models: list[GameModel] = []
        self.owner: Player | None = None

    def set_owner(self, owner: 'Player'):
        self.owner = owner
        for model in self.models:
            model.owner = owner

    @property
    def quantity(self):
        return len(self.models)

    @property
    def strength(self):
        return sum([m.data.W for m in self.models]) / sum([m.profile.W for m in self.models])

    @property
    def objects(self):
        return [model.geometry for model in self.models]


class Player:
    def __init__(self, player_profile: PlayerProfile | None, team: int, units: list[GameUnit]):
        self.player_profile = player_profile
        self.team = team
        self.command_points: int = 0
        self.objection_points: int = 0
        self.is_winner: bool = False
        self.units = units
        self.camera = GameCamera()
        self._set_owner()

    def _set_owner(self):
        for unit in self.units:
            unit.set_owner(self)


class GameState:
    def __init__(self):
        self.player_act: Player | None = None
        self.name: GAME_STATE_NAMES = GAME_STATE_NAMES.INITIAL
        self.battle_state: BattleState = BattleState()


class BattleState:
    def __init__(self):
        self.name: BATTLE_PHASE_NAMES = BATTLE_PHASE_NAMES.NONE
        self.turn_number: int = 0


class GameMap:
    def __init__(self, size: tuple[float, float], terrain: list[TerrainModel]):
        self.size = size
        self.size_x, self.size_y = size
        self.terrain = terrain
        self.borders = self._create_borders()

    @property
    def objects(self):
        objects = [model.geometry for model in self.terrain]
        objects.extend(self.borders)
        return objects

    def _create_borders(self):
        TL = (0, 0)
        TR = (0, self.size_y)
        BR = (self.size_x, self.size_y)
        BL = (self.size_x, 0)
        top = LineWithCollision(color=WHITE, position=0, start=TL, end=TR)
        bottom = LineWithCollision(color=WHITE, position=0, start=BR, end=BL)
        left = LineWithCollision(color=WHITE, position=0, start=TL, end=BL)
        right = LineWithCollision(color=WHITE, position=0, start=BR, end=TR)
        return top, bottom, left, right


class GameSettings:
    def __init__(self, mode: GAME_SETTINGS_MODE):
        self.mode = mode


class GameData:
    def __init__(self, map: GameMap, players: list[Player], game_state: GameState, settings: GameSettings):
        self.map = map
        self.players = players
        self.game_state: GameState = game_state
        self.settings = settings
        self.units = []
        for player in self.players:
            for unit in player.units:
                self.units.append(unit)

    @property
    def objects(self):
        objects = []
        _ = [objects.extend(unit.objects) for unit in self.units]
        objects.extend(self.map.objects)
        return objects

    @property
    def player_act(self):
        return self.game_state.player_act
