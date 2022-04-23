from typing import List

from core import Card


class DiscardPile:
    cards: List[Card]

    def __init__(self):
        self.cards = []

    def discard(self, card: Card):
        self.cards.append(card)
