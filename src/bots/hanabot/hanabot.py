import logging

from bots.domain.decision import DecisionMaking, PlayDecision, DiscardDecision, Decision, SuitClueDecision
from bots.domain.model.action import ClueAction
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.hanabot.blackboard import Blackboard
from bots.hanabot.conventions.convention import Conventions

logger = logging.getLogger(__name__)

SAVE_CLUE_ENABLED = False


class Hanabot(DecisionMaking):
    def __init__(self, conventions: Conventions):
        self.conventions = conventions
        self.blackboard = Blackboard()

    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        """
        1. wipe
        2. interpret actions
        3. make decision
        """
        self.blackboard.wipe_for_new_turn(current_game_state, history)

        current_game_state = self.interpret_actions()

        next_player_hand = current_game_state.other_player_hands[0]
        next_player_chop = self.conventions.find_card_on_chop(next_player_hand)

        if SAVE_CLUE_ENABLED and current_game_state.can_give_clue() and current_game_state.is_critical(next_player_chop.real_card):
            return self.conventions.find_save(next_player_chop, next_player_hand)

        # if possible card if playable or already played, play it (good touch principle)
        for slot, card in enumerate(current_game_state.my_hand):
            if card.is_clued and current_game_state.is_possibly_playable(card):
                return PlayDecision(slot)

        if current_game_state.can_give_clue():
            owner_slot_cards = current_game_state.find_playable_cards()
            for possible_decision in self.conventions.find_play_clue(owner_slot_cards, current_game_state):
                return possible_decision

        if current_game_state.can_discard():
            return DiscardDecision(self.conventions.find_chop(current_game_state.my_hand))

        return SuitClueDecision(next_player_hand[0].real_card.suit, 1)

    def interpret_actions(self) -> RelativeGameState:
        """
        1. For each action
            - Match and resolve interpretation with expected action
            - Match interpretation with unexpected action
            - Find new interpretation
            - Log non-interpretable actions
        2. Write notes on cards
        """

        for action in self.blackboard.uninterpreted_actions:
            if isinstance(action, ClueAction) and action.recipient == self.blackboard.current_game_state.my_hand.owner_name:
                logger.debug(f"Trying to understand {action}")
                interpretation = self.conventions.find_new_interpretations(action, self.blackboard)
                if interpretation:
                    self.blackboard.write_new_interpretation(interpretation[0])
                else:
                    logger.debug(f"Could not understand {action}")

        self.blackboard.write_notes_on_cards()
        # TODO reapply interpretations on hand

        return self.blackboard.current_game_state
