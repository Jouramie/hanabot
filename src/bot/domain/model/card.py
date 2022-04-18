from dataclasses import dataclass
from enum import auto, Enum


class Suit(Enum):
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()
    PURPLE = auto()

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
        else:
            raise ValueError("Invalid suit")


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
            raise ValueError(f"Invalid rank value: {value}")


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank


all_cards = [Card(suit, rank) for suit in Suit for rank in Rank]
