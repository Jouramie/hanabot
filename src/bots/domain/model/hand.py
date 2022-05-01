from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sized, Iterator, Type

from core import Card, Rank, Suit
from core.card import all_possible_cards

Slot: Type = int
DrawId: Type = int


@dataclass(frozen=True)
class HandCard:
    # Without interpretation, only basic clue information
    possible_cards: frozenset[Card]
    is_clued: bool
    draw_id: DrawId
    real_card: Card | None = None
    notes_on_cards: set[Card] = field(default_factory=set)

    @staticmethod
    def unknown_card(draw_id: DrawId = 0) -> HandCard:
        return HandCard(frozenset(all_possible_cards()), False, draw_id)

    @staticmethod
    def clued_card(suit: Suit | None = None, rank: Rank | None = None, draw_id: DrawId = 0) -> HandCard:
        if suit is not None and rank is not None:
            return HandCard(frozenset(all_possible_cards(suit, rank)), True, draw_id)
        elif suit is not None:
            return HandCard(frozenset(all_possible_cards(suits=suit)), True, draw_id)
        elif rank is not None:
            return HandCard(frozenset(all_possible_cards(ranks=rank)), True, draw_id)

    @staticmethod
    def unknown_real_card(card: Card) -> HandCard:
        return HandCard(frozenset(all_possible_cards()), False, 0, real_card=card)

    @staticmethod
    def clued_real_card(card: Card, suit_known: bool = False, rank_known: bool = False, draw_id: DrawId = 0) -> HandCard:
        if suit_known and rank_known:
            return HandCard(frozenset({card}), True, draw_id, real_card=card)
        elif suit_known:
            return HandCard(frozenset(all_possible_cards(suits=card.suit)), True, draw_id, real_card=card)
        elif rank_known:
            return HandCard(frozenset(all_possible_cards(ranks=card.rank)), True, draw_id, real_card=card)

    @staticmethod
    def known_real_card(card: Card, draw_id: DrawId = 0) -> HandCard:
        return HandCard.clued_real_card(card, True, True, draw_id)

    def __post_init__(self):
        self.notes_on_cards.update(self.possible_cards)

    def is_real(self, suit_or_rank: Suit | Rank) -> bool:
        return self.real_card is not None and self.real_card.matches(suit_or_rank)

    def __repr__(self):
        return f"{self.draw_id} -> {self.real_card if self.real_card is not None else self.possible_cards}"

    def is_known(self, suit_or_rank: Suit | Rank) -> bool:
        return all(card.matches(suit_or_rank) for card in self.possible_cards)


@dataclass(frozen=True)
class Hand(Iterable[HandCard], Sized):
    owner_name: str
    cards: tuple[HandCard, ...]

    @staticmethod
    def create_unknown_hand(player_name: str, size: int = 5) -> Hand:
        return Hand(player_name, tuple(HandCard.unknown_card() for i in range(size)))

    @staticmethod
    def create_unknown_real_hand(player_name: str, cards: Iterable[Card]) -> Hand:
        return Hand(player_name, tuple(HandCard.unknown_real_card(card) for card in cards))

    def __iter__(self) -> Iterator[HandCard]:
        return iter(self.cards)

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def get_real(self, suit_or_rank: Suit | Rank) -> Iterable[HandCard]:
        for card in self:
            if card.is_real(suit_or_rank):
                yield card

    def __repr__(self):
        return f"{self.owner_name} {self.cards})"

    # FIXME this do not seem right... It this really a hand concern to update the interpretations?
    def add_interpretation(self, interpretation: dict[DrawId, set[Card]]):
        for card in self:
            if card.draw_id in interpretation:
                card.notes_on_cards.intersection_update(interpretation[card.draw_id])

    def find_most_probable(self, cards: list[Card]) -> list[HandCard]:
        most_probable = []
        for card in cards:
            for hand_card in self:
                if hand_card.is_clued and hand_card not in most_probable and (hand_card.is_known(card.suit) or hand_card.is_known(card.rank)):
                    most_probable.append(hand_card)

        return most_probable
