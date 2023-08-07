from dataclasses import dataclass

from logic.handlers.camera_handler import CameraHandler
from logic.handlers.charge_handler import ChargeHandler
from logic.handlers.command_handler import CommandHandler
from logic.handlers.fight_handler import FightHandler
from logic.handlers.initial_handler import InitialHandler
from logic.handlers.move_handler import MoveHandler
from logic.handlers.shoot_handler import ShootHandler


@dataclass
class Handlers:

    def __init__(self, game_loop):
        self.loop = game_loop
        self.camera = CameraHandler(game_loop)
        self.command = CommandHandler(game_loop)
        self.move = MoveHandler(game_loop)
        self.shoot = ShootHandler(game_loop)
        self.charge = ChargeHandler(game_loop)
        self.fight = FightHandler(game_loop)
        self.initial = InitialHandler(game_loop)

