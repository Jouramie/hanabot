from typing import List

from simulator.game.hand_card import HandCard


class Player:
    name: str
    hand: List[HandCard]

    def __init__(self, name: str):
        self.name = name
        self.hand = []

    def __str__(self):
        return self.name
