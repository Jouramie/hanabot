from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

from frozendict import frozendict


class Suit(Enum):
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()
    PURPLE = auto()
    TEAL = auto()

    @staticmethod
    def value_of(s: str) -> Suit:
        suit = suit_abbreviation_mapping.get(s.lower())

        if suit is None:
            raise ValueError(f"Invalid suit: {s}")

        return suit

    def __repr__(self) -> str:
        return self.short_name()

    def short_name(self) -> str:
        return self.name[0:1].lower()


suit_abbreviation_mapping = frozendict(
    {
        "b": Suit.BLUE,
        "bl": Suit.BLUE,
        "g": Suit.GREEN,
        "gr": Suit.GREEN,
        "y": Suit.YELLOW,
        "ye": Suit.YELLOW,
        "r": Suit.RED,
        "re": Suit.RED,
        "p": Suit.PURPLE,
        "pu": Suit.PURPLE,
        "t": Suit.TEAL,
        "te": Suit.TEAL,
    }
)


class Rank(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()

    @staticmethod
    def value_of(value: int | str):
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

    @property
    def short_name(self) -> str:
        if self is Rank.ONE:
            return "1"
        elif self is Rank.TWO:
            return "2"
        elif self is Rank.THREE:
            return "3"
        elif self is Rank.FOUR:
            return "4"
        elif self is Rank.FIVE:
            return "5"

    @property
    def number_value(self) -> int:
        if self is Rank.ONE:
            return 1
        if self is Rank.TWO:
            return 2
        if self is Rank.THREE:
            return 3
        if self is Rank.FOUR:
            return 4
        if self is Rank.FIVE:
            return 5

    def __repr__(self) -> str:
        return self.short_name


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def __repr__(self) -> str:
        return f"{self.suit.short_name()}{self.rank.name}"
