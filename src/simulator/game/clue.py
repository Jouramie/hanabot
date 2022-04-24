from core.card import Rank, Suit, Card


class Clue:
    turn: int
    giver_name: str
    receiver_name: str
    touched_slots: set[int] = set()

    def touches_card(self, card: Card):
        pass


class ColorClue(Clue):
    suit: Suit

    def __init__(self, suit: Suit, receiver_name: str, giver_name: str, turn: int):
        self.suit = suit
        self.receiver_name = receiver_name
        self.giver_name = giver_name
        self.turn = turn

    def touches_card(self, card: Card):
        return self.suit == card.suit


class RankClue(Clue):
    rank: Rank

    def __init__(self, rank: Rank, receiver_name: str, giver_name: str, turn: int):
        self.rank = rank
        self.receiver_name = receiver_name
        self.giver_name = giver_name
        self.turn = turn

    def touches_card(self, card: Card):
        return self.rank == card.rank
