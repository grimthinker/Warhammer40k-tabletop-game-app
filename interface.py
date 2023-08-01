from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import GameLoop


class GameInterface:
    def __init__(self, loop: 'GameLoop', elements: 'InterfaceElements | None' = None):
        self.loop = loop
        self.elements = elements if elements else InterfaceElements()


@dataclass
class InterfaceElements:
    dragging_lines: list = field(default_factory=list)
    move_lines: list = field(default_factory=list)
    interactive: list = field(default_factory=list)

    @property
    def all(self):
        return self.interactive + self.dragging_lines + self.move_lines

