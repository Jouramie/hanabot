import logging

from bots.domain.decision import DecisionMaking, PlayDecision, DiscardDecision, Decision, SuitClueDecision
from bots.domain.model.action import ClueAction, PlayAction
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

    def discard_chop(self, current_game_state: RelativeGameState) -> DiscardDecision:
        return DiscardDecision(self.get_my_chop_slot(current_game_state))

    def get_my_chop_slot(self, current_game_state: RelativeGameState) -> int:
        return self.get_player_chop_slot(current_game_state.my_hand)

    def get_player_chop_slot(self, player_hand: Hand) -> int:
        for slot in range(len(player_hand) - 1, 0, -1):
            if not player_hand[slot].is_clued:
                return slot

        return -1