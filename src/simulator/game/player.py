from typing import List

from core import Card


class Player:
    name: str
    hand: List[Card]

    def __init__(self, name: str):
        self.name = name
        self.hand = []

    def __str__(self):
        return self.name
