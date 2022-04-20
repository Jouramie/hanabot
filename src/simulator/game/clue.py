from core.card import Rank, Suit, Card
from simulator.game.player import Player


class Clue:
    turn: int
    giver: Player
    receiver: Player

    def touches_card(self, card: Card):
        pass


class ColorClue(Clue):
    suit: Suit

    def __init__(self, suit: Suit, receiver: Player):
        self.suit = suit
        self.receiver = receiver

    def touches_card(self, card: Card):
        return self.suit == card.suit


class RankClue(Clue):
    rank: Rank

    def __init__(self, rank: Rank, receiver: Player):
        self.rank = rank
        self.receiver = receiver

    def touches_card(self, card: Card):
        return self.rank == card.rank
