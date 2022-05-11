from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Set, Sized

from frozendict import frozendict

from core import Rank, Suit, Card, Variant
from core.gamerules import get_suit_short_name


@dataclass(frozen=True)
class Stack:
    suit: Suit
    rank: Rank | None = None

    def __str__(self):
        stack_number = 0
        if self.rank is not None:
            stack_number = self.rank.number_value
        return get_suit_short_name(self.suit) + str(stack_number)

    def is_playable(self, rank: Rank) -> bool:
        return rank.is_playable_over(self.rank)

    def can_play(self, card: Card) -> bool:
        if self.suit != card.suit:
            raise ValueError(f"Stack is not {card.suit}")

        return self.is_playable(card.rank)

    def is_already_played(self, rank: Rank) -> bool:
        return self.rank is not None and self.rank >= rank

    @property
    def played_cards(self) -> list[Card]:
        if self.rank is None:
            return []
        return list(Card.inclusive_range(Card(self.suit, Rank.ONE), self.last_played_card))

    def get_ranks_already_played(self) -> list[Rank]:
        return list(card.rank for card in self.played_cards)

    @property
    def last_played_card(self) -> Card | None:
        if self.rank is None:
            return None
        return Card(self.suit, self.rank)

    @property
    def cards_left_to_play(self) -> list[Card]:
        if self.rank is Rank.FIVE:
            return []

        if self.rank is None:
            return list(Card.inclusive_range(Card(self.suit, Rank.ONE), Card(self.suit, Rank.FIVE)))

        return list(Card.inclusive_range(self.last_played_card.next_card, Card(self.suit, Rank.FIVE)))

    @property
    def stack_score(self) -> int:
        if self.rank is None:
            return 0
        return self.rank.number_value

    def play(self, card: Card) -> tuple[Stack, bool]:
        if not self.can_play(card):
            return self, False

        return Stack(self.suit, card.rank), True


@dataclass(frozen=True)
class Stacks(Sized):
    stack_by_suit: frozendict[Suit, Stack]

    @staticmethod
    def create_empty_stacks(suits: Iterable[Suit]) -> Stacks:
        return Stacks(frozendict({suit: Stack(suit) for suit in suits}))

    @staticmethod
    def create_from_cards(cards: Iterable[Card]) -> Stacks:
        return Stacks(frozendict({card.suit: Stack(card.suit, card.rank) for card in cards}))

    @staticmethod
    def create_from_dict(played_ranks: dict[Suit, Rank], suits: Iterable[Suit] = Variant.NO_VARIANT) -> Stacks:
        return Stacks({suit: Stack(suit, played_ranks.get(suit, None)) for suit in suits})

    def __len__(self) -> int:
        return len(self.stack_by_suit)

    def are_all_playable_or_already_played(self, possible_cards: Iterable[Card]) -> bool:
        return all(self.is_playable(card) or self.is_already_played(card) for card in possible_cards)

    def is_playable(self, card: Card) -> bool:
        stack = self.stack_by_suit.get(card.suit)
        if stack is None:
            raise ValueError(f"No stack for suit {card.suit}")

        return stack.is_playable(card.rank)

    def can_play(self, card: Card) -> bool:
        return self.is_playable(card)

    def is_already_played(self, card: Card) -> bool:
        stack = self.stack_by_suit.get(card.suit)
        if stack is None:
            raise ValueError(f"No stack for suit {card.suit}")

        return stack.is_already_played(card.rank)

    @property
    def played_cards(self) -> Set[Card]:
        return {card for stack in self.stack_by_suit.values() for card in stack.played_cards}

    @property
    def stacks_score(self) -> int:
        return sum(stack.stack_score for stack in self.stack_by_suit.values())

    def play(self, card: Card) -> tuple[Stacks, bool]:
        stack = self.stack_by_suit.get(card.suit)
        if stack is None:
            raise ValueError(f"No stack for suit {card.suit}")

        new_stacks, is_played = stack.play(card)
        if not is_played:
            return self, False

        return Stacks(self.stack_by_suit.set(card.suit, new_stacks)), True

    def last_card_played_on_stack(self, suit: Suit) -> Card | None:
        return self.stack_by_suit[suit].last_played_card

    def cards_left_to_play_on(self, suit: Suit) -> list[Card]:
        return self.stack_by_suit[suit].cards_left_to_play
