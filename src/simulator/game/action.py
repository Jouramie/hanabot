from dataclasses import dataclass

from simulator.game.card import Card
from simulator.game.clue import Clue
from simulator.game.player import Player


@dataclass(frozen=True)
class Action:
    turn: int
    actor: Player


@dataclass(frozen=True)
class ClueAction(Action):
    clue: Clue


@dataclass(frozen=True)
class PlayAction(Action):
    playedCard: Card
    cardSlot: int
    success: bool


@dataclass(frozen=True)
class DiscardAction(Action):
    discardedCard: Card
    cardSlot: int
