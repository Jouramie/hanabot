from bots.domain.decision import ClueDecision, RankClueDecision
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerCard, PlayerHand
from bots.hanabot.convention import Convention


class SingleCardPlayClueConvention(Convention):
    def find_play_clue(self, owner_slot_cards: tuple[int, int, PlayerCard], current_game_state: RelativeGameState) -> ClueDecision | None:
        owner, slot, player_card = owner_slot_cards

        hand: PlayerHand = current_game_state.other_player_hands[owner]

        rank = player_card.real_card.rank
        if len(hand.get_real(rank)) == 1:
            return RankClueDecision(rank, hand.owner_name)

        # TODO suit clues
        return None
