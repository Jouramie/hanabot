from dataclasses import dataclass

from simulator.game.card import Suit, Rank
from simulator.game.player import Player


class Clue:
    turn: int
    giver: Player
    receiver: Player


class ColorClue(Clue):
    suit: Suit


class RankClue(Clue):
    rank: Rank

    def __init__(self, rank: Rank, receiver: Player):
        self.rank = rank
        self.receiver = receiver
