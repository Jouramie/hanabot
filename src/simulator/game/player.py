from __future__ import annotations

from typing import List

from simulator.game.hand_card import HandCard


class Player:
    name: str
    hand: List[HandCard]

    def __init__(self, name: str, hand: List[HandCard] = None):
        if hand is None:
            hand = []
        self.name = name
        self.hand = hand

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name} {self.hand}"
