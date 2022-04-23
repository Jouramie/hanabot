from typing import List

from core.card import Card, Suit, Rank
from core.game_setup import all_possible_cards
from simulator.game.clue import Clue


class HandCard:
    real_card: Card
    received_clues: List[Clue]
    suits_in_game: List[Suit]
    possible_cards: List[Card]

    def __init__(self, card: Card, suits_in_game: List[Suit]):
        self.real_card = card
        self.suits_in_game = suits_in_game
        self.received_clues = []
        self.possible_cards = list(all_possible_cards(suits_in_game))

    def receive_clue(self, clue: Clue):
        self.possible_cards = \
            [card for card in self.possible_cards if clue.touches_card(card) == clue.touches_card(self.real_card)]
        self.received_clues.append(clue)

    def get_all_possible_cards(self) -> List[Card]:
        return self.possible_cards

    def get_all_possible_suits(self) -> List[Suit]:
        return list(set([card.suit for card in self.possible_cards]))

    def get_all_possible_ranks(self) -> List[Rank]:
        return list(set([card.rank for card in self.possible_cards]))

    def is_clued(self) -> bool:
        for clue in self.received_clues:
            if clue.touches_card(self.real_card):
                return True
        return False

    def __repr__(self):
        return self.real_card.short_name
