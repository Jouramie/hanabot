from dataclasses import dataclass
from typing import List
from simulator.game.handcard import HandCard


@dataclass
class Player:
    name: str
    hand: List[HandCard]

    def __init__(self, name: str):
        self.name = name
        self.hand = []
