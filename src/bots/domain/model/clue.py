from abc import ABC
from dataclasses import dataclass

from bots.domain.model.player import Slot
from core import Rank, Suit


@dataclass(frozen=True)
class AbstractClue(ABC):
    touched_slots: frozenset[Slot]


@dataclass(frozen=True)
class SuitClue(AbstractClue):
    suit: Suit

    def __repr__(self):
        return f"{self.suit.name} on slots {{{set(self.touched_slots)}}})"


@dataclass(frozen=True)
class RankClue(AbstractClue):
    rank: Rank

    def __repr__(self):
        return f"{self.rank.name} on slots {set(self.touched_slots)}"


Clue = SuitClue | RankClue
