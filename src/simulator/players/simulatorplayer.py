from abc import ABC, abstractmethod

from simulator.game.action import Action
from simulator.game.gamestate import GameState


class SimulatorPlayer(ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def start_new_game(self):
        pass

    @abstractmethod
    def play_turn(self, gamestate: GameState) -> Action:
        pass
