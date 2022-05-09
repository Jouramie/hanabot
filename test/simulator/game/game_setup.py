from typing import List

from core.card import Suit, Rank, Card


def get_player_names(num: int) -> List[str]:
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


def get_suits(num: int) -> tuple[Suit, ...]:
    if num == 3:
        return Suit.BLUE, Suit.GREEN, Suit.RED
    if num == 4:
        return Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW
    if num == 5:
        return Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW, Suit.PURPLE
    if num == 6:
        return Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW, Suit.PURPLE, Suit.TEAL


def get_ranks() -> tuple[Rank, ...]:
    return Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE


def get_possible_cards(suits) -> List[Card]:
    cards = []
    for suit in suits:
        for rank in get_ranks():
            cards.append(Card(suit, rank))

    return cards
