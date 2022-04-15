from typing import List

from simulator.game.card import Card


class Player:
    name: str
    hand: List[Card]

    def __init__(self, name: str):
        self.name = name
        self.hand = []
