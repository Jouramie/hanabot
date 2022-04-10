from dataclasses import dataclass
from enum import auto, Enum


class Suit(Enum):
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()
    PURPLE = auto()


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

    
