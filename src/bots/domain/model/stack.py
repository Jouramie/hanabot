from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from frozendict import frozendict

from core import Rank, Suit, Card


@dataclass(frozen=True)
class Stack:
    # TODO is this really needed?
    suit: Suit
    rank: Rank | None = None

    def is_playable(self, rank: Rank) -> bool:
        return rank.is_playable_over(self.rank)

    def is_already_played(self, rank: Rank) -> bool:
        return self.rank is not None and self.rank >= rank


@dataclass(frozen=True)
class Stacks:
    stack_by_suit: frozendict[Suit, Stack]

    @staticmethod
    def create_empty_stacks(suits: frozenset[Suit]) -> Stacks:
        return Stacks({suit: Stack(suit) for suit in suits})

    def are_all_playable_or_already_played(self, probable_cards: Iterable[Card]) -> bool:
        return all(self.is_playable(card) or self.is_already_played(card) for card in probable_cards)

    def is_playable(self, card: Card) -> bool:
        stack = self.stack_by_suit.get(card.suit)
        if stack is None:
            raise ValueError(f"No stack for suit {card.suit}")

        return stack.is_playable(card.rank)

    def is_already_played(self, card: Card) -> bool:
        stack = self.stack_by_suit.get(card.suit)
        if stack is None:
            raise ValueError(f"No stack for suit {card.suit}")

        return stack.is_already_played(card.rank)
