import logging

from bots.domain.decision import RankClueDecision, SuitClueDecision, ClueDecision
from bots.domain.model.action import ClueAction
from bots.domain.model.game_state import RelativeGameState, RelativePlayerNumber
from bots.domain.model.hand import HandCard, Hand, Slot
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions.convention import Convention

logger = logging.getLogger(__name__)


class SingleCardPlayClue(Convention):
    def __init__(self):
        super().__init__("single card play clue")

    def find_clue(self, card_to_clue: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[ClueDecision] | None:
        # TODO handle duplicate cards
        owner, slot, player_card = card_to_clue

        hand: Hand = current_game_state.player_hands[owner]

        suit = player_card.real_card.suit
        real_cards_with_suit = list(hand.get_real(suit))
        if len(real_cards_with_suit) == 1:
            decision = SuitClueDecision(suit, owner)
            logger.debug(f"{decision}.")
            return [decision]

        rank = player_card.real_card.rank
        real_cards_with_rank = list(hand.get_real(rank))
        if len(real_cards_with_rank) == 1:
            decision = RankClueDecision(rank, owner)
            logger.debug(f"{decision}.")
            return [decision]

        return None

    def find_interpretation(self, clue_action: ClueAction, current_game_state: RelativeGameState) -> Interpretation | None:
        if len(clue_action.touched_slots) != 1:
            return None

        (touched_draw_id,) = clue_action.touched_draw_ids
        touched_card = current_game_state.find_card_by_draw_id(touched_draw_id)
        if touched_card is None:
            return None

        playable_cards = {card for card in touched_card.possible_cards if current_game_state.is_playable(card)}

        if playable_cards:
            return Interpretation(
                clue_action,
                interpretation_type=InterpretationType.PLAY,
                explanation=self.name,
                notes_on_cards={touched_card.draw_id: set(playable_cards)},
            )

        return None
