from __future__ import annotations

from copy import deepcopy
from typing import List, Iterable

from core.card import Card, Suit, Rank, all_possible_cards
from simulator.game.clue import Clue
from util.profiling import timeit


class HandCard:
    draw_id: int
    real_card: Card
    received_clues: List[Clue]
    suits_in_game: Iterable[Suit]
    possible_cards: frozenset[Card]

    def __init__(
        self,
        draw_id: int,
        card: Card,
        suits_in_game: Iterable[Suit],
        is_clued: bool = False,
        received_clues: List[Clue] = None,
        possible_cards: frozenset[Card] = None,
    ):
        if received_clues is None:
            received_clues = []
        if possible_cards is None:
            possible_cards = all_possible_cards(suits_in_game)
        self.draw_id = draw_id
        self.real_card = card
        self.suits_in_game = suits_in_game
        self.is_clued = is_clued
        self.received_clues = received_clues
        self.possible_cards = possible_cards

    def receive_clue(self, clue: Clue) -> bool:
        is_touched = clue.touches_card(self.real_card)
        self.possible_cards = frozenset({card for card in self.possible_cards if clue.touches_card(card) == is_touched})
        self.received_clues.append(clue)
        self.is_clued |= is_touched
        return is_touched

    def get_all_possible_cards(self) -> List[Card]:
        return list(self.possible_cards)

    def get_all_possible_suits(self) -> List[Suit]:
        return list(set([card.suit for card in self.possible_cards]))

    def get_all_possible_ranks(self) -> List[Rank]:
        return list(set([card.rank for card in self.possible_cards]))

    def __repr__(self):
        return self.real_card.short_name

    @timeit(name="Simulator.HandCard.deepcopy")
    def __deepcopy__(self, memo):
        return HandCard(
            self.draw_id,
            self.real_card,
            self.suits_in_game,
            self.is_clued,
            timeit(name="Simulator.HandCard.clues_deepcopy", method=deepcopy)(self.received_clues, memo),
            self.possible_cards,
        )
