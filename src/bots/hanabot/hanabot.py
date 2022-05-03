import logging

from bots.domain.decision import DecisionMaking, PlayDecision, DiscardDecision, Decision, SuitClueDecision
from bots.domain.model.action import ClueAction, PlayAction, DiscardAction
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.hanabot.blackboard import Blackboard
from bots.hanabot.conventions.convention import Conventions

logger = logging.getLogger(__name__)

SAVE_CLUE_ENABLED = False


class Hanabot(DecisionMaking):
    def __init__(self, conventions: Conventions):
        self.conventions = conventions
        self.blackboard = Blackboard()

    def new_game(self):
        self.blackboard = Blackboard()

    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        """
        1. wipe
        2. interpret actions
        3. make decision
        """
        self.blackboard.wipe_for_new_turn(current_game_state, history)

        current_game_state = self.try_interpret_actions()

        return self.make_decision(current_game_state)

    def try_interpret_actions(self) -> RelativeGameState:
        try:
            return self.interpret_actions()
        except Exception as e:
            logger.exception(e)
            return self.blackboard.current_game_state

    def interpret_actions(self) -> RelativeGameState:
        """
        1. For each action
            - Find chop
            - Match and resolve interpretation with expected action
            - Match interpretation with unexpected action
            - Find new interpretation
            - Log non-interpretable actions
        2. Write notes on cards
        """
        for action in self.blackboard.uninterpreted_actions:
            self.blackboard.chop = self.conventions.find_chop(self.blackboard.my_hand)

            if isinstance(action, PlayAction) or isinstance(action, DiscardAction):
                for interpretation in self.blackboard.ongoing_interpretations.copy():
                    if action.draw_id not in interpretation.notes_on_cards:
                        continue

                    interpretation.played_cards.add(action.draw_id)
                    if interpretation.played_cards != interpretation.notes_on_cards.keys():
                        continue

                    logger.debug(f"{action} resolved interpretation {interpretation}.")
                    self.blackboard.move_interpretation_to_resolved(interpretation)

            elif isinstance(action, ClueAction):
                interpretation = self.conventions.find_new_interpretations(action, self.blackboard)
                if interpretation:
                    self.blackboard.write_new_interpretation(interpretation[0])
                else:
                    logger.debug(f"WTF is this Charles {action}")

        self.blackboard.write_notes_on_cards()

        return self.blackboard.current_game_state

    def make_decision(self, current_game_state: RelativeGameState) -> Decision:
        next_player_hand = current_game_state.other_player_hands[0]
        next_player_chop = self.conventions.find_card_on_chop(next_player_hand)

        if SAVE_CLUE_ENABLED and current_game_state.can_give_clue() and current_game_state.is_critical(next_player_chop.real_card):
            return self.conventions.find_save(next_player_chop, next_player_hand)

        # if possible card if playable or already played, play it (good touch principle)
        for slot, card in enumerate(current_game_state.my_hand):
            if card.is_clued and current_game_state.is_possibly_playable(card):
                return PlayDecision(slot)

        if current_game_state.can_give_clue():
            playable_cards = current_game_state.find_not_known_playable_cards()
            for possible_decision in self.conventions.find_play_clue(playable_cards, current_game_state):
                return possible_decision

        if current_game_state.can_discard():
            return DiscardDecision(self.conventions.find_chop(current_game_state.my_hand))

        return SuitClueDecision(next_player_hand[0].real_card.suit, 1)
