from random import shuffle
from typing import Iterable, List

from core import Suit, Card, Rank


def generate(suits: Iterable[Suit]) -> List[Card]:
    deck = []
    for suit in suits:
        deck.append(Card(suit, Rank.ONE))
        deck.append(Card(suit, Rank.ONE))
        deck.append(Card(suit, Rank.ONE))

        deck.append(Card(suit, Rank.TWO))
        deck.append(Card(suit, Rank.TWO))

        deck.append(Card(suit, Rank.THREE))
        deck.append(Card(suit, Rank.THREE))

        deck.append(Card(suit, Rank.FOUR))
        deck.append(Card(suit, Rank.FOUR))

        deck.append(Card(suit, Rank.FIVE))

    shuffle(deck)
    return deck
