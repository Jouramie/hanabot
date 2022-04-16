from dataclasses import dataclass

from simulator.game.gamestate import GameState


class GameResult:
    final_state: GameState

    def __init__(self, final_state: GameState):
        if not final_state.isOver:
            raise ValueError('Cannot generate result for an unfinished game')
        self.final_state = final_state

    @property
    def is_survival(self):
        return self.final_state.currentStrikes < 3

    @property
    def is_victory(self):
        return self.score == len(self.final_state.stacks) * 5

    @property
    def score(self):
        if self.is_survival:
            return self.played_cards
        return 0

    @property
    def played_cards(self):
        score = 0
        for stack in self.final_state.stacks.values():
            score = score + stack.stack_score()

        return score

