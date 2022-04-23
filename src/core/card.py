from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, Iterator

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
        return self.short_name

    @property
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

    def is_playable_over(self, already_played_rank: Rank | None) -> bool:
        if self is Rank.ONE:
            return already_played_rank is None
        elif self is Rank.TWO:
            return already_played_rank is Rank.ONE
        elif self is Rank.THREE:
            return already_played_rank is Rank.TWO
        elif self is Rank.FOUR:
            return already_played_rank is Rank.THREE
        elif self is Rank.FIVE:
            return already_played_rank is Rank.FOUR

    def __gt__(self, other):
        return self.number_value > other.number_value

    def __lt__(self, other):
        return self.number_value < other.number_value

    def __ge__(self, other):
        return self.number_value >= other.number_value

    def __le__(self, other):
        return self.number_value <= other.number_value

    def __repr__(self) -> str:
        return self.short_name


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def __repr__(self) -> str:
        return self.short_name

    def matches(self, suit_or_rank: Suit | Rank) -> bool:
        return self.suit is suit_or_rank or self.rank is suit_or_rank

    @property
    def short_name(self) -> str:
        return f"{self.suit.short_name}{self.rank.short_name}"

    def __eq__(self, other):
        return self.suit == other.suit and self.rank == other.rank


class Variant(Enum):
    NO_VARIANT = ((Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW, Suit.PURPLE),)
    SIX_SUITS = ((Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW, Suit.PURPLE, Suit.TEAL),)
    FOUR_SUITS = ((Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW),)
    THREE_SUITS = ((Suit.BLUE, Suit.GREEN, Suit.RED),)

    def __init__(self, suits: tuple[Suit, ...]):
        self.suits = suits

    @staticmethod
    def get_suits(num: int) -> Variant:
        if num == 3:
            return Variant.THREE_SUITS
        if num == 4:
            return Variant.FOUR_SUITS
        if num == 5:
            return Variant.NO_VARIANT
        if num == 6:
            return Variant.SIX_SUITS

    def __iter__(self) -> Iterator[Suit]:
        return iter(self.suits)

    def __len__(self) -> int:
        return len(self.suits)


def all_possible_cards(
    suits: Iterable[Suit] = Variant.NO_VARIANT,
    ranks: Iterable[Rank] = (Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE),
) -> Iterable[Card]:
    for suit in suits:
        for rank in ranks:
            yield Card(suit, rank)
