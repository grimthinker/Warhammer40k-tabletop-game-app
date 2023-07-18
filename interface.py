from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameLoop


class GameInterface:
    def __init__(self, loop: 'GameLoop'):
        self.loop = loop

