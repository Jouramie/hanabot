from dataclasses import dataclass

from simulator.game.gamestate import GameState


class GameResult:
    finalState: GameState
    score: int
    maxScore: int
    strikes: int

    @property
    def IsSurvival(self):
        return self.strikes < 3

    @property
    def IsVictory(self):
        return self.score == self.maxScore
