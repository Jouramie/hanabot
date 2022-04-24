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


@dataclass(frozen=True)
class RankClue(AbstractClue):
    rank: Rank


Clue = SuitClue | RankClue
