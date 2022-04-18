from dataclasses import dataclass
from enum import Enum, auto


class Suit(Enum):
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()
    PURPLE = auto()
    TEAL = auto()

    @staticmethod
    def from_char(char):
        if char == "b":
            return Suit.BLUE
        elif char == "g":
            return Suit.GREEN
        elif char == "y":
            return Suit.YELLOW
        elif char == "r":
            return Suit.RED
        elif char == "p":
            return Suit.PURPLE
        elif char == "t":
            return Suit.TEAL
        else:
            raise ValueError(f"Invalid suit: {char}")


class Rank(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()

    @staticmethod
    def from_char(value: int | str):
        if str(value) == "1":
            return Rank.ONE
        elif str(value) == "2":
            return Rank.TWO
        elif str(value) == "3":
            return Rank.THREE
        elif str(value) == "4":
            return Rank.FOUR
        elif str(value) == "5":
            return Rank.FIVE
        else:
            raise ValueError(f"Invalid rank: {value}")


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank
