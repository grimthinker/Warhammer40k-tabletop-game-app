from dataclasses import dataclass, field

from logic.classes import DInt


@dataclass
class AbilityProfile:
    pass


@dataclass
class WeaponBase:
    A: int | DInt = 1  # Attacks
    S: int = 1  # Strength
    AP: int = 0  # Armour penetration
    D: int | DInt = 1  # Damage
    use_limit: int | None = None


@dataclass
class RangedWeapon(WeaponBase):
    R: int | DInt = 1  # Range
    BS: int = 1  # Ballistic skill


@dataclass
class MeleeWeapon(WeaponBase):
    WS: int = 1  # Weapon skill


@dataclass
class RangedWeaponData(RangedWeapon):
    use_number: int = 0


@dataclass
class MeleeWeaponData(MeleeWeapon):
    use_number: int = 0


class Rule:
    pass


@dataclass
class Ability:
    tags: list[str] = field(default_factory=list)
    FNP: int | None = None


@dataclass
class GeometryData:
    forms: list


@dataclass
class TerrainProfile:
    H: float
    passable: bool
    can_be_stood_on: bool
    visibility_rule: Rule
    cover_rule: Rule
    geometry_data: GeometryData


@dataclass
class ModelProfile:
    M: int = 6  # Move
    T: int = 1  # Toughness
    Sv: int = 6  # Save
    InvSv: int | None = None  # Invulnerable save
    W: int = 1  # Wounds
    LD: int = 1  # Leadership
    OK: int = 1  # Objective control
    ranged_weapons: list[RangedWeapon] = field(default_factory=list)
    melee_weapons: list[MeleeWeapon] = field(default_factory=list)
    abilities: list[Ability] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    faction_keywords: list[str] = field(default_factory=list)
    wargear_options: list[str] = field(default_factory=list)
    leader: list['ModelProfile'] = field(default_factory=list)

    base: bool = True  # If True, model has a base. If False, model is represented as a Rectangle using length and width
    base_diameter: float = 1
    length: int | None = 1
    width: int | None = 1
    passable: bool = False
    can_be_stood_on: bool = False


class ModelData:
    def __init__(
            self,
            profile: ModelProfile,
            ranged_weapons: list[RangedWeaponData] | None = None,
            melee_weapons: list[MeleeWeaponData] | None = None,
            wargear: str | None = None,
            enhancement: str | None = None
    ):
        self.M = profile.M
        self.T = profile.T
        self.Sv = profile.Sv
        self.W = profile.W
        self.LD = profile.LD
        self.OK = profile.OK
        self.ranged_weapons = ranged_weapons if ranged_weapons else list()
        self.melee_weapons = melee_weapons if melee_weapons else list()
        self.enhancement = enhancement
        self.wargear = wargear

