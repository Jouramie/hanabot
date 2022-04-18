from enum import Enum, auto
from typing import Iterable

from frozendict import frozendict

from core import Suit, Rank, Card


def get_player_names(num: int) -> list[str]:
    if num == 2:
        return ["Alice", "Bob"]
    if num == 3:
        return ["Alice", "Bob", "Cathy"]
    if num == 4:
        return ["Alice", "Bob", "Cathy", "Donald"]
    if num == 5:
        return ["Alice", "Bob", "Cathy", "Donald", "Emily"]
    if num == 6:
        return ["Alice", "Bob", "Cathy", "Donald", "Emily", "Frank"]


class Variant(Enum):
    NO_VARIANT = auto()
    SIX_SUITS = auto()
    FOUR_SUITS = auto()
    THREE_SUITS = auto()


suits_per_variant = frozendict(
    {
        Variant.NO_VARIANT: (Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW, Suit.PURPLE),
        Variant.SIX_SUITS: (Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW, Suit.PURPLE, Suit.TEAL),
        Variant.FOUR_SUITS: (Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW),
        Variant.THREE_SUITS: (Suit.BLUE, Suit.GREEN, Suit.RED),
    }
)


def get_suits(num: int) -> tuple[Suit, ...]:
    if num == 3:
        return suits_per_variant[Variant.THREE_SUITS]
    if num == 4:
        return suits_per_variant[Variant.FOUR_SUITS]
    if num == 5:
        return suits_per_variant[Variant.NO_VARIANT]
    if num == 6:
        return suits_per_variant[Variant.SIX_SUITS]


def all_cards(
    suits: Iterable[Suit] = suits_per_variant[Variant.NO_VARIANT],
    ranks: Iterable[Rank] = (Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE),
) -> list[Card]:
    for suit in Suit:
        for rank in Rank:
            yield Card(suit, rank)
