from dataclasses import dataclass
from typing import List

from simulator.game.gameresult import GameResult
from simulator.game.gamestate import GameState
from simulator.simulatorplayer import SimulatorPlayer


class Controller:
    currentGame: GameState

    def NewGame(self, players : List[SimulatorPlayer]) -> GameState:
        pass

    def PlayTurn(self) -> GameState:
        pass

    def PlayUntilGameOver(self) -> GameResult:
        pass

    def IsGameOver(self) -> bool:
        pass

    def GetGameResult(self) -> GameResult:
        pass