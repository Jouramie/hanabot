from dataclasses import dataclass

from bots.domain.model.clue import SuitClue, RankClue
from core import Card


@dataclass(frozen=True)
class PlayAction:
    played_card: Card


@dataclass(frozen=True)
class DiscardAction:
    discarded_card: Card


@dataclass(frozen=True)
class ClueAction:
    recipient: str
    clue: SuitClue | RankClue


Action = PlayAction | DiscardAction | ClueAction
