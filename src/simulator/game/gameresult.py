from __future__ import annotations

from simulator.game.gamestate import GameState


class GameResult:
    def __init__(self, is_victory: bool, is_survival: bool, score: int, max_score: int, played_cards: int):
        self.is_victory = is_victory
        self.is_survival = is_survival
        self.score = score
        self.max_score = max_score
        self.played_cards = played_cards

    @staticmethod
    def from_game_state(game_state: GameState) -> GameResult:
        if not game_state.status.is_over:
            raise ValueError("Cannot generate result for an unfinished game")
        is_survival = game_state.status.strikes < 3
        played_cards = sum(stack.stack_score() for stack in game_state.play_area.stacks.values())
        max_score = len(game_state.play_area.stacks) * 5
        score = played_cards if is_survival else 0
        is_victory = score == max_score
        return GameResult(is_victory, is_survival, score, max_score, played_cards)

    def __repr__(self):
        if self.is_victory:
            return f"The team has won with a max score of {str(self.score)}."
        elif self.is_survival:
            return f"The team has survived with a score of {str(self.score)} out of {str(self.max_score)}."
        else:
            return f"The team has struck out after playing {str(self.played_cards)} cards."
