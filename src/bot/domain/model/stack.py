from dataclasses import dataclass
from typing import Dict, Set

from bot.domain.model.card import Rank, Suit


@dataclass(frozen=True)
class Stack:
    rank: Rank | None = None


# FIXME this should be frozen
@dataclass
class Stacks:
    stackBySuit: Dict[Suit, Stack]

    def __init__(self, suits: Set[Suit]):
        self.stackBySuit = {suit: Stack() for suit in suits}
