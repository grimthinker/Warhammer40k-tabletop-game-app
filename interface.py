from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameLoop


class GameInterface:
    def __init__(self, loop: 'GameLoop', elements: list | None = None):
        self.loop = loop
        self.elements = elements if elements else list()

