from core import Suit, Rank
from simulator.game.player import Player


class Clue:
    turn: int
    giver: Player
    receiver: Player


class ColorClue(Clue):
    suit: Suit

    def __init__(self, suit: Suit, receiver: Player):
        self.suit = suit
        self.receiver = receiver


class RankClue(Clue):
    rank: Rank

    def __init__(self, rank: Rank, receiver: Player):
        self.rank = rank
        self.receiver = receiver
