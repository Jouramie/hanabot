import logging

from bots.domain.decision import DecisionMaking, PlayDecision, DiscardDecision, Decision, SuitClueDecision
from bots.domain.model.action import ClueAction
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.hanabot.conventions.convention import Conventions

logger = logging.getLogger(__name__)

SAVE_CLUE_ENABLED = False


class Hanabot(DecisionMaking):
    def __init__(self, conventions: Conventions):
        self.conventions = conventions

    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        """
        choose action (all hands + interpreted hands + stacks

        perform action

        """
        current_game_state = self.interpret_clues(current_game_state, history)

        next_player_hand = current_game_state.other_player_hands[0]
        next_player_chop = self.conventions.find_card_on_chop(next_player_hand)

        if SAVE_CLUE_ENABLED and current_game_state.can_give_clue() and current_game_state.is_critical(next_player_chop.real_card):
            return self.conventions.find_save(next_player_chop, next_player_hand)

        # if possible card if playable or already played, play it (good touch principle)
        for slot, card in enumerate(current_game_state.my_hand):
            if current_game_state.is_possibly_playable(card):
                return PlayDecision(slot)

        if current_game_state.can_give_clue():
            owner_slot_cards = current_game_state.find_not_clued_playable_cards()
            for possible_decision in self.conventions.find_play_clue(owner_slot_cards, current_game_state):
                return possible_decision

        if current_game_state.can_discard():
            return DiscardDecision(self.conventions.find_chop(current_game_state.my_hand))

        # Waste clue
        return SuitClueDecision(next_player_hand[0].real_card.suit, 1)

    def interpret_clues(self, current_game_state: RelativeGameState, history: GameHistory) -> RelativeGameState:
        # TODO this should go alot deeper than 4 turns
        actions_since_last_turn = history.action_history[current_game_state.turn_number - len(current_game_state.player_hands) : current_game_state.turn_number]

        for action in actions_since_last_turn:
            if isinstance(action, ClueAction) and action.recipient == current_game_state.my_hand.owner_name:
                logger.debug(f"Trying to understand {action.clue}")
                interpretation = self.conventions.find_interpretations(action.clue, current_game_state)
                if interpretation:
                    current_game_state.my_hand.add_interpretation(interpretation[0])
                else:
                    logger.debug(f"Could not understand {action.clue}")

        return current_game_state
