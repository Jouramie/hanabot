from abc import ABC, abstractmethod

from simulator.game.action import Action
from core.state.gamestate import GameState
from simulator.game.game import Game


class SimulatorPlayer(ABC):
    name: str

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def new_game(self):
        pass

    @abstractmethod
    def play_turn(self, game: Game) -> Action:
        pass
