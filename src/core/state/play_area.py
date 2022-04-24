from typing import Dict, Iterable

from core import Suit, Card
from core.state.stack import Stack


class PlayArea:
    stacks: Dict[Suit, Stack]

    def __init__(self, suits: Iterable[Suit]):
        self.stacks = {}
        for suit in suits:
            self.stacks[suit] = Stack(suit)

    def can_play(self, card: Card) -> bool:
        return self.stacks[card.suit].can_play(card)