from dataclasses import dataclass

from bots.domain.model.hand import Slot
from core import Card, Suit, Rank


@dataclass(frozen=True)
class PlayAction:
    played_card: Card


@dataclass(frozen=True)
class DiscardAction:
    discarded_card: Card


@dataclass(frozen=True)
class SuitClueAction:
    recipient: str
    touched_slots: frozenset[Slot]
    suit: Suit

    def __repr__(self):
        return f"{self.suit.name} on slots {set(self.touched_slots)})"


@dataclass(frozen=True)
class RankClueAction:
    recipient: str
    touched_slots: frozenset[Slot]
    rank: Rank

    def __repr__(self):
        return f"{self.rank.name} on slots {set(self.touched_slots)}."


ClueAction = SuitClueAction | RankClueAction
Action = PlayAction | DiscardAction | ClueAction
