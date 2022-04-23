from bots.domain.decision import ClueDecision, RankClueDecision
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerCard, PlayerHand, RelativePlayerId
from bots.hanabot.convention import Convention


class SingleCardPlayClueConvention(Convention):
    def __init__(self):
        super().__init__("single_card_play_clue")

    def find_play_clue(self, owner_slot_cards: tuple[RelativePlayerId, int, PlayerCard], current_game_state: RelativeGameState) -> ClueDecision | None:
        owner, slot, player_card = owner_slot_cards

        hand: PlayerHand = current_game_state.player_hands[owner]

        rank = player_card.real_card.rank
        real_cards_with_rank = list(hand.get_real(rank))
        if len(real_cards_with_rank) == 1:
            return RankClueDecision(rank, owner)

        # TODO suit clues
        return None
