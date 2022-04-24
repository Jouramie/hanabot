from core.card import Rank, Suit, Card


class Clue:
    turn: int
    giver_name: str
    receiver_name: str
    touched_slots: set[int]

    def __init__(self, turn: int, giver_name: str, receiver_name: str, touched_slots=None):
        if touched_slots is None:
            touched_slots = set()
        self.turn = turn
        self.giver_name = giver_name
        self.receiver_name = receiver_name
        self.touched_slots = touched_slots

    def touches_card(self, card: Card):
        pass


class ColorClue(Clue):
    suit: Suit

    def __init__(self, suit: Suit, receiver_name: str, giver_name: str, turn: int):
        super().__init__(turn, giver_name, receiver_name)
        self.suit = suit

    def touches_card(self, card: Card):
        return self.suit == card.suit

    def __repr__(self):
        return f"{self.giver_name} gave {self.suit.name} to {self.receiver_name}"


class RankClue(Clue):
    rank: Rank

    def __init__(self, rank: Rank, receiver_name: str, giver_name: str, turn: int):
        super().__init__(turn, giver_name, receiver_name)
        self.rank = rank

    def touches_card(self, card: Card):
        return self.rank == card.rank

    def __repr__(self):
        return f"{self.giver_name} gave {self.rank.name} to {self.receiver_name}"
