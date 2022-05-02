import logging

from bots.domain.decision import RankClueDecision, SuitClueDecision, ClueDecision
from bots.domain.model.action import ClueAction
from bots.domain.model.game_state import RelativeGameState, RelativePlayerNumber
from bots.domain.model.hand import HandCard, Hand, Slot
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions.convention import Convention

logger = logging.getLogger(__name__)


class SingleCardPlayClueConvention(Convention):
    def __init__(self):
        super().__init__("Single card rank play clue")

    def find_play_clue(self, owner_slot_cards: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[ClueDecision] | None:
        # TODO handle duplicate cards
        owner, slot, player_card = owner_slot_cards

        hand: Hand = current_game_state.player_hands[owner]

        suit = player_card.real_card.suit
        real_cards_with_suit = list(hand.get_real(suit))
        if len(real_cards_with_suit) == 1:
            return [SuitClueDecision(suit, owner)]

        rank = player_card.real_card.rank
        real_cards_with_rank = list(hand.get_real(rank))
        if len(real_cards_with_rank) == 1:
            return [RankClueDecision(rank, owner)]

        return None

    def find_interpretation(self, clue_action: ClueAction, current_game_state: RelativeGameState) -> Interpretation | None:
        if len(clue_action.touched_slots) != 1 or clue_action.recipient != current_game_state.my_hand.owner_name:
            return None

        (touched_slot,) = clue_action.touched_slots
        touched_card = current_game_state.my_hand[touched_slot]

        playable_cards = {card for card in touched_card.possible_cards if current_game_state.is_playable(card)}

        if playable_cards:
            logger.debug(f"{clue_action} could be a {self.name}.")
            return Interpretation(
                clue_action, interpretation_type=InterpretationType.PLAY, convention_name=self.name, notes_on_cards={touched_card.draw_id: set(playable_cards)}
            )

        return None
