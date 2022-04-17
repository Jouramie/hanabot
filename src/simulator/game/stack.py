from dataclasses import dataclass

from simulator.game.card import Card
from simulator.game.gamerules import get_suit_short_name
from simulator.game.rank import Rank
from simulator.game.suit import Suit


class Stack:
    suit: Suit
    last_played: Card | None

    def __init__(self, suit: Suit):
        self.suit = suit
        self.last_played = None

    def __str__(self):
        stack_number = 0
        if self.last_played is not None:
            stack_number = self.last_played.number_value
        return get_suit_short_name(self.suit) + str(stack_number)

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