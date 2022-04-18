from core import Suit, Rank
from simulator.game.gamerules import get_suit_short_name


class Card:
    suit: Suit
    rank: Rank

    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return get_suit_short_name(self.suit) + str(self.number_value)

    @property
    def number_value(self) -> int:
        if self.rank == Rank.ONE:
            return 1
        if self.rank == Rank.TWO:
            return 2
        if self.rank == Rank.THREE:
            return 3
        if self.rank == Rank.FOUR:
            return 4
        if self.rank == Rank.FIVE:
            return 5
