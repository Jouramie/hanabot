from dataclasses import dataclass

from simulator.game.gamestate import GameState


class GameResult:
    final_state: GameState

    def __init__(self, final_state: GameState):
        if not final_state.status.is_over:
            raise ValueError('Cannot generate result for an unfinished game')
        self.final_state = final_state

    @property
    def is_survival(self) -> bool:
        return self.final_state.status.strikes < 3

    @property
    def is_victory(self) -> bool:
        return self.score == self.max_score

    @property
    def score(self) -> int:
        if self.is_survival:
            return self.played_cards
        return 0

    @property
    def max_score(self) -> int:
        return len(self.final_state.play_area.stacks) * 5

    @property
    def played_cards(self) -> int:
        score = 0
        for stack in self.final_state.play_area.stacks.values():
            score = score + stack.stack_score()

        return score
