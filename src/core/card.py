from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable, Iterator

from frozendict import frozendict


class Rank(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()

    @staticmethod
    def value_of(value: int | str):
        value = str(value)
        if value == "1":
            return Rank.ONE
        elif value == "2":
            return Rank.TWO
        elif value == "3":
            return Rank.THREE
        elif value == "4":
            return Rank.FOUR
        elif value == "5":
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

    @property
    def next(self) -> Rank:
        if self is Rank.ONE:
            return Rank.TWO
        elif self is Rank.TWO:
            return Rank.THREE
        elif self is Rank.THREE:
            return Rank.FOUR
        elif self is Rank.FOUR:
            return Rank.FIVE

    @property
    def previous(self) -> Rank:
        if self is Rank.TWO:
            return Rank.ONE
        elif self is Rank.THREE:
            return Rank.TWO
        elif self is Rank.FOUR:
            return Rank.THREE
        elif self is Rank.FIVE:
            return Rank.FOUR

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


default_distribution = frozendict(
    {
        Rank.ONE: 3,
        Rank.TWO: 2,
        Rank.THREE: 2,
        Rank.FOUR: 2,
        Rank.FIVE: 1,
    }
)


class Suit(Enum):
    BLUE = auto()
    GREEN = auto()
    YELLOW = auto()
    RED = auto()
    PURPLE = auto()
    TEAL = auto()

    def __init__(self, _):
        self.distribution = default_distribution

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

    def amount_of(self, rank: Rank) -> int:
        return self.distribution[rank]


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

_cards = {}


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    @staticmethod
    def create(suit: Suit, rank: Rank) -> Card:
        return Card(suit, rank)

    @staticmethod
    def inclusive_range(*args: Card) -> Iterable[Card]:
        if len(args) == 2:
            _, stop = args
        elif len(args) == 1:
            stop = args[0]
        else:
            raise ValueError("Invalid number of arguments")

        for card in Card.range(*args):
            yield card
        yield stop

    @staticmethod
    def range(*args: Card) -> Iterable[Card]:
        if len(args) == 2:
            i, stop = args
        elif len(args) == 1:
            i, stop = Card(args[0].suit, Rank.ONE), args[0]
        else:
            raise ValueError("Invalid number of arguments")

        while i != stop:
            yield i
            i = i.next_card

    def __new__(cls, *args, _cache={}):  # noqa
        if _cache.get(args) is not None:
            return _cache[args]
        card = super(Card, cls).__new__(cls)
        card.__init__(*args)  # noqa
        _cache[args] = card
        return card

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        memo[id(self)] = self
        return self

    def matches(self, suit_or_rank: Suit | Rank) -> bool:
        return self.suit is suit_or_rank or self.rank is suit_or_rank

    @property
    def short_name(self) -> str:
        return f"{self.suit.short_name}{self.rank.short_name}"

    @property
    def number_of_copies(self) -> int:
        return self.suit.amount_of(self.rank)

    def __eq__(self, other):
        return isinstance(other, Card) and self.suit == other.suit and self.rank == other.rank

    def __repr__(self) -> str:
        return self.short_name

    def __hash__(self) -> int:
        return Card.get_card_hash(self)

    def __iter__(self):
        yield self.suit
        yield self.rank

    def is_playable_over(self, card: Card) -> bool:
        return self.previous_card == card

    @property
    def next_card(self) -> Card:
        next_rank = self.rank.next
        return self.create(self.suit, next_rank) if next_rank is not None else None

    @property
    def previous_card(self) -> Card:
        previous_rank = self.rank.previous
        return self.create(self.suit, previous_rank) if previous_rank is not None else None

    @staticmethod
    def get_suit_and_rank_hash(suit: Suit, rank: Rank) -> int:
        suit_hash = hash(suit)
        rank_hash = hash(rank)
        full_hash = hash((suit_hash * 33) + rank_hash)
        return full_hash

    @staticmethod
    def get_card_hash(card: Card) -> int:
        return Card.get_suit_and_rank_hash(card.suit, card.rank)


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

    def __contains__(self, item):
        return item in self.suits


def all_possible_cards(
    suits: Iterable[Suit] | Suit = Variant.NO_VARIANT,
    ranks: Iterable[Rank] | Rank = (Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE),
    _cache: dict[tuple[Iterable[Suit], Iterable[Rank]], frozenset[Card]] = {},  # noqa
) -> frozenset[Card]:
    if (suits, ranks) in _cache:
        return _cache[suits, ranks]

    if isinstance(suits, Suit):
        suits = (suits,)
    if isinstance(ranks, Rank):
        ranks = (ranks,)

    possible_cards = frozenset({Card.create(suit, rank) for suit in suits for rank in ranks})
    _cache[suits, ranks] = possible_cards
    return possible_cards


def amount_of_cards(variant: Iterable[Suit]) -> int:
    return sum(suit.amount_of(rank) for suit in variant for rank in Rank)
