from simulator.game.gamestate import GameState


class GameResult:
    def __init__(self, final_state: GameState):
        if not final_state.status.is_over:
            raise ValueError("Cannot generate result for an unfinished game")
        final_state = final_state
        self.is_survival = final_state.status.strikes < 3
        self.played_cards = sum(stack.stack_score() for stack in final_state.play_area.stacks.values())
        self.max_score = len(final_state.play_area.stacks) * 5
        self.score = self.played_cards if self.is_survival else 0
        self.is_victory = self.score == self.max_score

    def __repr__(self):
        if self.is_victory:
            return f"The team has won with a max score of {str(self.score)}"
        elif self.is_survival:
            return f"The team has survived with a score of {str(self.score)} out of {str(self.max_score)}"
        else:
            return f"The team has struck out after playing {str(self.played_cards)}"
