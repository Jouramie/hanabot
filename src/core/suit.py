from __future__ import annotations
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