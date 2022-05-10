import logging

from bots.domain.decision import SuitClueDecision, ClueDecision, RankClueDecision
from bots.domain.model.action import ClueAction
from bots.domain.model.game_state import RelativeGameState, RelativePlayerNumber, Turn
from bots.domain.model.hand import HandCard, Hand, Slot
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions.convention import Convention

logger = logging.getLogger(__name__)


class PlayClue(Convention):
    def __init__(self):
        super().__init__("play clue")

    def find_clue(self, card_to_clue: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[ClueDecision] | None:
        owner, slot, player_card = card_to_clue
        if player_card.is_fully_known or current_game_state.is_already_clued(player_card.real_card):
            return None

        hand: Hand = current_game_state.player_hands[owner]
        valid_decisions = []

        suit, rank = player_card.real_card
        touched_slots_cards = list(hand.get_real(suit))
        if self.is_valid_clue_for(touched_slots_cards, card_to_clue, current_game_state):
            decision = SuitClueDecision(suit, owner)
            logger.debug(f"{decision}.")
            valid_decisions.append(decision)

        touched_slots_cards = list(hand.get_real(rank))
        if self.is_valid_clue_for(touched_slots_cards, card_to_clue, current_game_state):
            decision = RankClueDecision(rank, owner)
            logger.debug(f"{decision}.")
            valid_decisions.append(decision)

        return valid_decisions if valid_decisions else None

    def is_valid_clue_for(
        self, touched_slots_cards: list[tuple[Slot, HandCard]], card_to_clue: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState
    ) -> bool:
        owner, slot, player_card = card_to_clue
        hand: Hand = current_game_state.player_hands[owner]
        touched_slots, touched_cards = zip(*touched_slots_cards)

        focus = self.document.find_focus(touched_slots, hand)
        if focus is not slot:
            return False

        if len(touched_cards) != len(set(card.real_card for card in touched_cards)):
            return False

        not_clued_touched_cards = [card for card in touched_cards if not card.is_clued]
        if any(not current_game_state.is_eventually_playable(card.real_card) for card in not_clued_touched_cards):
            return False

        if any(current_game_state.is_already_clued(card.real_card) for card in not_clued_touched_cards):
            return False

        return True

    def find_interpretation(self, turn: Turn) -> Interpretation | None:
        if not isinstance(turn.action, ClueAction):
            return

        clue = turn.action
        touched_card = self.find_focus_card(clue, turn.game_state.find_player_hand(clue.recipient))
        if touched_card is None:
            return

        playable_cards = {card for card in touched_card.possible_cards if clue.matches(card) and turn.game_state.is_playable(card)}

        if playable_cards:
            return Interpretation(
                turn,
                interpretation_type=InterpretationType.PLAY,
                explanation=self.name,
                notes_on_cards={touched_card.draw_id: playable_cards},
            )

        return
