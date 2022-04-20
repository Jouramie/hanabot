from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Iterable

from core import Rank, Suit, Card


@dataclass(frozen=True)
class Stack:
    suit: Suit
    rank: Rank | None = None

    def is_playable(self, rank: Rank) -> bool:
        # return rank.is_playable_over(self.rank)
        pass

    def is_already_played(self, rank: Rank) -> bool:
        pass
        # return self.rank is not None and self.rank >= rank


# FIXME this should be frozen
@dataclass
class Stacks:
    stack_by_suit: Dict[Suit, Stack]

    @staticmethod
    def empty_stacks(suits: Set[Suit]) -> Stacks:
        return Stacks({suit: Stack(suit) for suit in suits})

    def are_all_playable_or_already_played(self, probable_cards: Iterable[Card]) -> bool:
        # return all(self.is_playable(card) or self.is_already_played(card) for card in probable_cards)
        pass

    def is_playable(self, card: Card) -> bool:
        # return self.stack_by_suit[card.suit].is_playable(card.rank)
        pass

    def is_already_played(self, card: Card) -> bool:
        # return self.stack_by_suit[card.suit].is_already_played(card.rank)
        pass
