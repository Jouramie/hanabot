from abc import ABC, abstractmethod

from simulator.game.action import Action
from simulator.game.gamestate import GameState


class SimulatorPlayer(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def play_turn(self, gamestate: GameState) -> Action:
        pass
