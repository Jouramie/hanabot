from __future__ import annotations

from dataclasses import dataclass
from random import shuffle
from typing import Iterable, Iterator

from core.card import Card, Rank, Variant


@dataclass(frozen=True)
class Deck:
    _cards: list[Card]
    variant: Variant = Variant.NO_VARIANT

    def __post_init__(self):
        self._cards.reverse()

    @staticmethod
    def generate(variant: Variant = Variant.NO_VARIANT) -> Deck:
        cards = []
        for suit in variant:
            cards.append(Card(suit, Rank.ONE))
            cards.append(Card(suit, Rank.ONE))
            cards.append(Card(suit, Rank.ONE))

            cards.append(Card(suit, Rank.TWO))
            cards.append(Card(suit, Rank.TWO))

            cards.append(Card(suit, Rank.THREE))
            cards.append(Card(suit, Rank.THREE))

            cards.append(Card(suit, Rank.FOUR))
            cards.append(Card(suit, Rank.FOUR))

            cards.append(Card(suit, Rank.FIVE))

        shuffle(cards)
        return Deck(cards, variant)

    @staticmethod
    def starting_with(cards: Iterable[Card] | Card, variant: Variant = Variant.NO_VARIANT) -> Deck:
        if isinstance(cards, Card):
            cards = [cards]

        other_cards = Deck.generate(variant)._cards
        for card in cards:
            other_cards.remove(card)

        shuffle(other_cards)
        return Deck(list(cards) + other_cards, variant)

    def draw(self) -> Card:
        return self._cards.pop()

    def is_empty(self) -> bool:
        return not self._cards

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


def generate(variant: Variant) -> Deck:
    return Deck.generate(variant)
