from bots.domain.decision import ClueDecision, RankClueDecision
from bots.domain.model.clue import Clue
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerCard, PlayerHand, RelativePlayerNumber, Slot
from bots.hanabot.conventions.convention import Convention, Interpretation


class SingleCardPlayClueConvention(Convention):
    def __init__(self):
        super().__init__("single_card_play_clue")

    def find_play_clue(self, owner_slot_cards: tuple[RelativePlayerNumber, Slot, PlayerCard], current_game_state: RelativeGameState) -> ClueDecision | None:
        owner, slot, player_card = owner_slot_cards

        hand: PlayerHand = current_game_state.player_hands[owner]

        rank = player_card.real_card.rank
        real_cards_with_rank = list(hand.get_real(rank))
        if len(real_cards_with_rank) == 1:
            return RankClueDecision(rank, owner)

        # TODO suit clues
        return None

    def find_interpretation(self, clue: Clue, current_game_state: RelativeGameState) -> Interpretation | None:
        pass
