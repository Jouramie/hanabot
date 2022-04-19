from typing import List

from core.card import Card
from core.hand_card import HandCard
from core.rank import Rank
from core.suit import Suit
from simulator.game.clue import Clue


class SimulationHandCard(HandCard):
    real_card: Card
    received_clues: List[Clue]

    def __init__(self, card: Card, suits_in_game: List[Suit]):
        pass

    def receive_clue(self, clue: Clue):
        pass

    def get_all_possible_cards(self) -> List[Card]:
        pass

    def get_all_possible_suits(self) -> List[Suit]:
        pass

    def get_all_possible_ranks(self) -> List[Rank]:
        pass
