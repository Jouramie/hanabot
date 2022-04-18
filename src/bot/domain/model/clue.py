from dataclasses import dataclass
from typing import Set

from core import Suit, Rank


@dataclass(frozen=True)
class SuitClue:
    hand_positions: Set[int]
    suit: Suit


@dataclass(frozen=True)
class RankClue:
    hand_positions: Set[int]
    rank: Rank
