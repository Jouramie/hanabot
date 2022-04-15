from dataclasses import dataclass

from bot.domain.card import Rank, Suit


@dataclass(frozen=True)
class Clue:
    handPosition: int


@dataclass(frozen=True)
class ColorClue(Clue):
    suit: Suit


@dataclass(frozen=True)
class RankClue(Clue):
    rank: Rank
