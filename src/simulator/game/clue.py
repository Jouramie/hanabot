from dataclasses import dataclass

from simulator.game.player import Player


@dataclass(frozen=True)
class Clue:
    turn: int
    giver: Player
    receiver: Player


@dataclass(frozen=True)
class ColorClue(Clue):
    suit: Suit


@dataclass(frozen=True)
class RankClue(Clue):
    rank: Rank
