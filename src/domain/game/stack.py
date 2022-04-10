from dataclasses import dataclass

from src.domain.card import Rank
from src.domain.game.card import Suit, Card


@dataclass(frozen=True)
class Stack:
    suit: Suit
    lastPlayed: Card

    def can_play(self, card):
        return card.canPlayOn(self.lastPlayed)