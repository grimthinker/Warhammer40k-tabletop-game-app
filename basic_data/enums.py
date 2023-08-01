from enum import StrEnum


class ExtendedStrEnum(StrEnum):
    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))

class ActionTypes(ExtendedStrEnum):
    DRAGGING_MODEL = 'dragging model'
    DRAGGING_CAMERA = 'dragging camera'
    ROTATING_CAMERA = 'rotating camera'


class ControlEventTypes(ExtendedStrEnum):
    UNDEFINED = 'not defined'
    SCROLL = 'mousewheel scroll'

    MOUSE_MAIN_UP = 'mouse left button up'
    MOUSE_MIDDLE_UP = 'mouse middle button up'
    MOUSE_SEC_UP = 'mouse button right up'
    MOUSE_BACK_UP = 'mouse back button up'
    MOUSE_FORTH_UP = 'mouse forward button up'

    MOUSE_MAIN_DOWN = 'mouse left button down'
    MOUSE_MIDDLE_DOWN = 'mouse middle button down'
    MOUSE_SEC_DOWN = 'mouse right button down'
    MOUSE_BACK_DOWN = 'mouse back button down'
    MOUSE_FORTH_DOWN = 'mouse forward button down'

    MOUSE_MOTION = 'mouse motion'


class MODE_NAMES(ExtendedStrEnum):
    MENU = 'menu'
    GAME = 'game'


class GAME_STATE_NAMES(ExtendedStrEnum):
    INITIAL = 'initial'
    #
    #
    #
    #
    BATTLE = 'battle'
    CONCLUSION = 'conclusion'
    ENDED = 'ended'


class BATTLE_PHASE_NAMES(ExtendedStrEnum):
    NONE = 'none'
    COMMAND = 'command phase'
    MOVE = 'move phase'
    SHOOT = 'shoot phase'
    CHARGE = 'charge phase'
    FIGHT = 'fight phase'


class GAME_SETTINGS_MODE(ExtendedStrEnum):
    SINGLE = 'singleplayer'
    MULTY = 'multyplayer'


class COLLISION_TYPE(ExtendedStrEnum):
    TO_STAND = 'to_stand'
    TO_MOVE_THROUGH = 'to_move_through'
