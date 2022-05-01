import logging

from bots.domain.decision import DecisionMaking, DiscardDecision, Decision
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.hand import Hand

logger = logging.getLogger(__name__)


class Machinabi(DecisionMaking):
    def __init__(self):
        pass

    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        if current_game_state.clue_count < 8:
            return self.discard_chop(current_game_state)
        pass

    def discard_chop(self, current_game_state: RelativeGameState) -> Decision:
        chop_slot = self.get_my_chop_slot(current_game_state)
        if -1 < chop_slot < len(current_game_state.my_hand):
            return DiscardDecision(chop_slot)

        return self.locked_hand_decision(current_game_state)

    def locked_hand_decision(self, current_game_state: RelativeGameState):
        if current_game_state.clue_count > 0:
            return self.stall_clue(current_game_state)
        return self.anxiety_play(current_game_state)

    def get_my_chop_slot(self, current_game_state: RelativeGameState) -> int:
        return self.get_player_chop_slot(current_game_state.my_hand)

    def get_player_chop_slot(self, player_hand: Hand) -> int:
        for slot in range(len(player_hand) - 1, -1, -1):
            if not player_hand[slot].is_clued:
                return slot

        return -1

    def stall_clue(self, current_game_state: RelativeGameState):
        pass

    def anxiety_play(self, current_game_state: RelativeGameState):
        pass
