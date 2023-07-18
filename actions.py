from dataclasses import dataclass, field

from enums import ActionTypes
from gamedata import GameObject


@dataclass
class DragData:
    dragged_obj: GameObject
    start_pos: tuple[float, float]
    start_pos_z: int
    end_pos: tuple[float, float] | None = None
    end_pos_z: int | None = None


@dataclass
class Action:
    type: ActionTypes
    data: DragData | None = None
    complete: bool = False

