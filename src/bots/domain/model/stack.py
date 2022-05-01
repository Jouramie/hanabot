from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Set

from frozendict import frozendict

from core import Rank, Suit, Card, Variant


@dataclass(frozen=True)
class Stack:
    # TODO is this really needed?
    suit: Suit
    rank: Rank | None = None

    def is_playable(self, rank: Rank) -> bool:
        return rank.is_playable_over(self.rank)

    def is_already_played(self, rank: Rank) -> bool:
        return self.rank is not None and self.rank >= rank

    @property
    def played_cards(self) -> Set[Card]:
        if self.rank is None:
            return set()
        return {Card(self.suit, Rank.value_of(rank)) for rank in range(1, self.rank.number_value + 1)}


@dataclass(frozen=True)
class Stacks:
    stack_by_suit: frozendict[Suit, Stack]

    @staticmethod
    def create_empty_stacks(suits: Iterable[Suit]) -> Stacks:
        return Stacks({suit: Stack(suit) for suit in suits})

    @staticmethod
    def create_from_cards(cards: Iterable[Card]) -> Stacks:
        return Stacks(frozendict({card.suit: Stack(card.suit, card.rank) for card in cards}))

    @staticmethod
    def create_from_dict(played_ranks: dict[Suit, Rank], suits: Iterable[Suit] = Variant.NO_VARIANT) -> Stacks:
        return Stacks({suit: Stack(suit, played_ranks.get(suit, None)) for suit in suits})

    def are_all_playable_or_already_played(self, possible_cards: Iterable[Card]) -> bool:
        return all(self.is_playable(card) or self.is_already_played(card) for card in possible_cards)

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

    @property
    def played_cards(self) -> Set[Card]:
        return {card for stack in self.stack_by_suit.values() for card in stack.played_cards}
