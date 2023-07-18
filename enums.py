from enum import StrEnum


class ActionTypes(StrEnum):
    DRAGGING_MODEL = 'dragging model'
    DRAGGING_CAMERA = 'dragging camera'


class ControlEventTypes(StrEnum):
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




