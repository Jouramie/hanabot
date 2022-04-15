from dataclasses import dataclass
from enum import auto, Enum

class Suit(Enum):
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()
    PURPLE = auto()
    TEAL = auto()


class Rank(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()

@dataclass
class Card:
    suit: Suit
    rank: Rank

    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    @property
    def number_value(self) -> int:
        if self.rank == Rank.ONE:
            return 1
        if self.rank == Rank.TWO:
            return 2
        if self.rank == Rank.THREE:
            return 3
        if self.rank == Rank.FOUR:
            return 4
        if self.rank == Rank.FIVE:
            return 5