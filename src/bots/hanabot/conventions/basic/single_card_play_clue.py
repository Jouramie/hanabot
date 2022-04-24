from bots.domain.decision import RankClueDecision
from bots.domain.model.clue import RankClue
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerCard, PlayerHand, RelativePlayerNumber, Slot
from bots.hanabot.conventions.convention import Convention, Interpretation, InterpretationType


class SingleCardRankPlayClueConvention(Convention):
    def __init__(self):
        super().__init__("Single card rank play clue")

    def find_play_clue(self, owner_slot_cards: tuple[RelativePlayerNumber, Slot, PlayerCard], current_game_state: RelativeGameState) -> RankClueDecision | None:
        owner, slot, player_card = owner_slot_cards

        hand: PlayerHand = current_game_state.player_hands[owner]

        rank = player_card.real_card.rank
        real_cards_with_rank = list(hand.get_real(rank))
        if len(real_cards_with_rank) == 1:
            return RankClueDecision(rank, owner)

        return None

    def find_interpretation(self, clue: RankClue, current_game_state: RelativeGameState) -> Interpretation | None:
        if len(clue.touched_slots) != 1:
            return None

        (touched_slot,) = clue.touched_slots
        touched_card = current_game_state.my_hand[touched_slot]

        playable_cards = {card for card in touched_card.possible_cards if current_game_state.is_playable(card)}

        if playable_cards:
            return Interpretation(InterpretationType.PLAY, self.name, {touched_slot: set(playable_cards)})

        return None
