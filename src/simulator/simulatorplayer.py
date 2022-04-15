from dataclasses import dataclass
from simulator.game.action import Action


class SimulatorPlayer:

    def play_turn(self, gamestate) -> Action:
        pass

    def get_name(self) -> str:
        pass
