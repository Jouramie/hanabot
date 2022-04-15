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


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def canPlayOn(self, other_card):
        if self.suit != other_card.suit:
            return False
        if self.rank == Rank.ONE:
            return other_card is None
        return self.rank == other_card.rank + 1