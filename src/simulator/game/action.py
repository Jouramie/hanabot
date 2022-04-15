from dataclasses import dataclass

from simulator.game.card import Card
from simulator.game.clue import Clue
from simulator.game.player import Player


class Action:
    turn: int
    actor: Player


class ClueAction(Action):
    clue: Clue

    def __init__(self, clue: Clue):
        self.clue = clue

class PlayAction(Action):
    playedCard: Card
    cardSlot: int
    success: bool

    def __init__(self, slot: int):
        self.cardSlot = slot


class DiscardAction(Action):
    discardedCard: Card
    cardSlot: int

    def __init__(self, slot: int):
        self.cardSlot = slot
