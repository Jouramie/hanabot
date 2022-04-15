from dataclasses import dataclass

from simulator.game.card import Suit, Card


@dataclass(frozen=True)
class Stack:
    suit: Suit
    lastPlayed: Card

    def can_play(self, card):
        return card.can_play_on(self.lastPlayed)