from dataclasses import dataclass

from simulator.game.card import Suit, Card


@dataclass
class Stack:
    suit: Suit
    lastPlayed: Card | None

    def __init__(self, suit: Suit):
        self.suit = suit
        self.lastPlayed = None

    def can_play(self, card):
        return card.can_play_on(self.lastPlayed)

    def play(self, card):
        if self.can_play(card):
            self.lastPlayed = card