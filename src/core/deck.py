from __future__ import annotations

from dataclasses import dataclass
from random import shuffle
from typing import Iterable, Iterator, Sized, Union, Container

from core.card import Card, Rank, Variant, Suit, amount_of_cards


@dataclass(frozen=True)
class Deck:
    _cards: list[Card]
    suits: Union[Iterable[Suit], Container[Suit], Sized] = Variant.NO_VARIANT

    def __post_init__(self):
        self._cards.reverse()

    @staticmethod
    def generate(suits: Iterable[Suit] = Variant.NO_VARIANT) -> Deck:
        cards = []
        for suit in suits:
            cards.append(Card.create(suit, Rank.ONE))
            cards.append(Card.create(suit, Rank.ONE))
            cards.append(Card.create(suit, Rank.ONE))

            cards.append(Card.create(suit, Rank.TWO))
            cards.append(Card.create(suit, Rank.TWO))

            cards.append(Card.create(suit, Rank.THREE))
            cards.append(Card.create(suit, Rank.THREE))

            cards.append(Card.create(suit, Rank.FOUR))
            cards.append(Card.create(suit, Rank.FOUR))

            cards.append(Card.create(suit, Rank.FIVE))

        shuffle(cards)
        return Deck(cards, suits=suits)

    @staticmethod
    def empty(suits: Iterable[Suit] = Variant.NO_VARIANT) -> Deck:
        cards = []
        return Deck(cards, suits=suits)

    @staticmethod
    def starting_with(cards: Iterable[Card] | Card, suits: Iterable[Suit] = Variant.NO_VARIANT) -> Deck:
        if isinstance(cards, Card):
            cards = [cards]
        else:
            cards = list(cards)

        other_cards = Deck.generate(suits)._cards
        for card in cards:
            other_cards.remove(card)

        shuffle(other_cards)
        return Deck(cards + other_cards, suits=suits)

    @staticmethod
    def from_starting_hands(starting_hands: list[list[Card]], suits: Iterable[Suit] = Variant.NO_VARIANT) -> Deck:
        deck_start = []
        for slot in reversed(range(0, len(starting_hands[0]))):
            for starting_hand in starting_hands:
                deck_start.append(starting_hand[slot])

        return Deck.starting_with(deck_start, suits)

    def draw(self) -> tuple[int, Card]:
        return amount_of_cards(self.suits) - len(self), self._cards.pop()

    def is_empty(self) -> bool:
        return not self._cards

    def number_cards(self) -> int:
        return len(self._cards)

    def __iter__(self) -> Iterator[Card]:
        return iter(self._cards[::-1])

    def __getitem__(self, item):
        return self._cards[::-1][item]

    def __len__(self) -> int:
        return len(self._cards)

    def __eq__(self, other: Deck) -> bool:
        return isinstance(other, Deck) and self._cards == other._cards

    def __ne__(self, other):
        return not self == other
