from dataclasses import dataclass

from simulator.game.card import Suit, Card, Rank


class Stack:
    suit: Suit
    lastPlayed: Card | None

    def __init__(self, suit: Suit):
        self.suit = suit
        self.lastPlayed = None

    def stack_score(self) -> int:
        if self.lastPlayed is None:
            return 0
        return self.lastPlayed.number_value

    def can_play(self, card) -> bool:
        if card.suit != self.suit:
            return False
        if self.lastPlayed is None:
            return card.rank == Rank.ONE
        return self.lastPlayed.number_value == card.number_value - 1

    def play(self, card) -> bool:
        if self.can_play(card):
            self.lastPlayed = card
            return True
        return False