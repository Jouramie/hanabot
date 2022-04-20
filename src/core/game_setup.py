from enum import Enum, auto
from typing import Iterable

from frozendict import frozendict

from core.card import Card, Rank, Suit

player_names_per_player_number: dict[int, tuple[str, ...]] = frozendict(
    {
        2: ("Alice", "Bob"),
        3: ("Alice", "Bob", "Cathy"),
        4: ("Alice", "Bob", "Cathy", "Donald"),
        5: ("Alice", "Bob", "Cathy", "Donald", "Emily"),
        6: ("Alice", "Bob", "Cathy", "Donald", "Emily", "Frank"),
    }
)


class Variant(Enum):
    NO_VARIANT = auto()
    SIX_SUITS = auto()
    FOUR_SUITS = auto()
    THREE_SUITS = auto()


suits_per_variant: dict[Variant : tuple[Suit, ...]] = frozendict(
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


def all_possible_cards(
    suits: Iterable[Suit] = suits_per_variant[Variant.NO_VARIANT],
    ranks: Iterable[Rank] = (Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE),
) -> Iterable[Card]:
    for suit in suits:
        for rank in ranks:
            yield Card(suit, rank)
