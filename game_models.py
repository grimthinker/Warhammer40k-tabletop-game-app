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
    use_limit: int | None = None


@dataclass
class RangedWeapon(WeaponBase):
    R: int = 1  # Range
    BS: int = 1  # Ballistic skill


@dataclass
class MeleeWeapon(WeaponBase):
    WS: int = 1  # Weapon skill


@dataclass
class RangeWeaponData(RangedWeapon):
    use_number: int = 0


@dataclass
class MeleeWeaponData(MeleeWeapon):
    use_number: int = 0


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
    abilities: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    faction_keywords: list[str] = field(default_factory=list)
    wargear_options: list[str] = field(default_factory=list)
    leader: list['ModelProfile'] = field(default_factory=list)

    base: bool = True  # If True, model has a base. If False, model is represented as a Rectangle using length and width
    base_diameter: float = 1
    length: int | None = 1
    width: int | None = 1


@dataclass
class ModelData:
    M: int = 6  # Current Move
    T: int = 1  # Current Toughness
    Sv: int = 6  # Current Save
    W: int = 1  # Current Wounds
    LD: int = 1  # Current Leadership
    OK: int = 1  # Current Objective control
    ranged_weapons: list[RangeWeaponData] = field(default_factory=list)  # Current Weapons
    melee_weapons: list[MeleeWeaponData] = field(default_factory=list)
    wargear: str | None = None  # Current wargear


class BaseModel:
    def __init__(
            self,
            profile: ModelProfile,
            data: ModelData,
            draggable: bool = False
    ):
        self.profile = profile
        self.data = data
        self.draggable = draggable

