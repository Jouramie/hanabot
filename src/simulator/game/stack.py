from dataclasses import dataclass

from simulator.game.card import Suit, Card, Rank


class Stack:
    suit: Suit
    last_played: Card | None

    def __init__(self, suit: Suit):
        self.suit = suit
        self.last_played = None

    def stack_score(self) -> int:
        if self.last_played is None:
            return 0
        return self.last_played.number_value

    def can_play(self, card) -> bool:
        if card.suit != self.suit:
            return False
        if self.last_played is None:
            return card.rank == Rank.ONE
        return self.last_played.number_value == card.number_value - 1

    def play(self, card) -> bool:
        if self.can_play(card):
            self.last_played = card
            return True
        return False