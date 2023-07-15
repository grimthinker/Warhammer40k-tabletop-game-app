from dataclasses import dataclass, field


@dataclass
class AbilityProfile:
    pass


@dataclass
class WeaponBase:
    A: int = 1  # Attacks
    S: int = 1  # Strength
    AP: int = 0  # Armour penetration
    D: int = 1  # Damage
    shot_limit: int | None = None


@dataclass
class RangedWeapon(WeaponBase):
    R: int = 1  # Range
    BS: int = 1  # Ballistic skill


@dataclass
class MeleeWeapon(WeaponBase):
    WS: int = 1  # Weapon skill


@dataclass
class ModelProfile:
    M: int = 1  # Move
    T: int = 1  # Toughness
    Sv: int = 6  # Save
    InvSv: int | None = None  # Invulnerable save
    W: int = 1  # Wounds
    LD: int = 1  # Leadership
    OK: int = 1  # Objective control
    ranged_weapons: list[RangedWeapon] = field(default_factory=list)
    melee_weapons: list[MeleeWeapon] = field(default_factory=list)
    abilities: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    faction_keywords: list[str] = field(default_factory=list)
    wargear_options: list[str] = field(default_factory=list)
    wargear: str | None = None
    leader: list['ModelProfile'] = field(default_factory=list)


class BaseModel:
    def __init__(
            self,
            model_profile: ModelProfile,
            draggable: bool = False
    ):
        self.model_profile = model_profile
        self.draggable = draggable

