from dataclasses import dataclass

from core.rank import Rank
from core.suit import Suit


@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank

    def __repr__(self) -> str:
        return f"{self.suit.short_name()}{self.rank.name}"
