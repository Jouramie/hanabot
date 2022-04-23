from __future__ import annotations

from dataclasses import dataclass
from random import shuffle
from typing import Iterable, Iterator, Sized, Union

from core.card import Card, Rank, Variant, Suit


@dataclass(frozen=True)
class Deck:
    _cards: list[Card]
    suits: Union[Iterable[Suit], Sized] = Variant.NO_VARIANT

    def __post_init__(self):
        self._cards.reverse()

    @staticmethod
    def generate(suits: Iterable[Suit] = Variant.NO_VARIANT) -> Deck:
        cards = []
        for suit in suits:
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
        return Deck(cards, suits)

    @staticmethod
    def starting_with(cards: Iterable[Card] | Card, suits: Iterable[Suit] = Variant.NO_VARIANT) -> Deck:
        if isinstance(cards, Card):
            cards = [cards]

        other_cards = Deck.generate(suits)._cards
        for card in cards:
            other_cards.remove(card)

        shuffle(other_cards)
        return Deck(list(cards) + other_cards, suits)

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
