from typing import TYPE_CHECKING

from models.profile import TerrainProfile, ModelProfile, ModelData
from basic_data.source import RED
from geometry.collision import CircleWithCollision, RectangleWithCollision

if TYPE_CHECKING:
    from logic.collision import CollisionMixin
    from gamedata import Player


class BasicModel:
    def __init__(
        self,
        profile: ModelProfile | TerrainProfile | None = None,
        effects: list | None = None,
    ):
        self.profile = profile
        self.effects = effects if effects else list()
        self.draggable = False
        self.owner: Player | None = None
        self.geometry: 'CollisionMixin | None' = None

    @property
    def passable(self):
        if self.profile:
            return self.profile.passable
        return False

    @property
    def can_be_stood_on(self):
        if self.profile:
            return self.profile.can_be_stood_on
        return False


class GameModel(BasicModel):
    def __init__(
        self,
        profile: ModelProfile | TerrainProfile | None = None,
        data: ModelData | None = None,
        position: tuple[float, float] = (0, 0),
        color: tuple[int, int] = RED
    ):
        super().__init__(profile)
        self.data = data
        self.geometry = make_geometry(self.profile, position, color)
        self.geometry.model = self


class TerrainModel(BasicModel):
    def __init__(
            self,
            profile: ModelProfile | TerrainProfile | None = None,
            position: tuple[float, float] = (0, 0),
            color: tuple[int, int] = RED
    ):
        super().__init__(profile)
        self.geometry = make_terrain_geometry(self.profile, position, color)
        self.geometry.model = self


def make_terrain_geometry(profile, position, color):
    for form in profile.geometry_data.forms:
        make_geometry(form, position, color)


def make_geometry(profile, position, color):
    if hasattr(profile, "base"):
        return CircleWithCollision(
            color=color,
            position=position,
            size=profile.base_diameter
        )
    else:
        return RectangleWithCollision(
            color=color,
            position=position,
            size=profile.length,
            width=profile.width,
            angle=0
        )
