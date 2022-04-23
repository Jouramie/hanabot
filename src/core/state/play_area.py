from typing import Dict, List

from core import Suit
from core.state.stack import Stack


class PlayArea:
    stacks: Dict[Suit, Stack]

    def __init__(self, suits: List[Suit]):
        self.stacks = {}
        for suit in suits:
            self.stacks[suit] = Stack(suit)