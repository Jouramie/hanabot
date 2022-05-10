from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class ClueType(Enum):
    SAVE = auto()
    PLAY = auto()
    STALL = auto()
    FIX = auto()


@dataclass(frozen=False)
class AnalysedClue:
    clue_type: ClueType

    @staticmethod
    def save_clue() -> AnalysedClue:
        return AnalysedClue(ClueType.SAVE)

    @staticmethod
    def play_clue() -> AnalysedClue:
        return AnalysedClue(ClueType.PLAY)