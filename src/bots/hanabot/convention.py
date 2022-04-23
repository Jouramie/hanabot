from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from bots.domain.decision import Decision, RankClueDecision, SuitClueDecision
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerHand, PlayerCard, RelativePlayerId
from core import Rank


class Convention(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def find_play_clue(self, owner_slot_cards: tuple[int, int, PlayerCard], current_game_state: RelativeGameState) -> Decision | None:
        pass


@dataclass(frozen=True)
class Conventions:
    conventions: Iterable[Convention]

    def find_save(self, card: PlayerCard, player_hand: PlayerHand) -> Decision:
        # TODO do better
        if card.real_card.rank == Rank.FIVE:
            return RankClueDecision(Rank.FIVE, player_hand.owner)

        if card.real_card.rank == Rank.TWO:
            return RankClueDecision(Rank.TWO, player_hand.owner)

        return SuitClueDecision(card.real_card.suit, player_hand.owner)

    def find_chop(self, player_hand: PlayerHand) -> int:
        # TODO that's not the chop lol
        return len(player_hand) - 1

    def find_card_on_chop(self, player_hand: PlayerHand) -> PlayerCard:
        return player_hand[self.find_chop(player_hand)]

    def find_play_clue(self, owner_slot_cards: Iterable[tuple[RelativePlayerId, int, PlayerCard]], current_game_state: RelativeGameState) -> Iterable[Decision]:
        for owner_slot_card in owner_slot_cards:
            for convention in self.conventions:
                decision = convention.find_play_clue(owner_slot_card, current_game_state)
                if decision is not None:
                    yield decision
