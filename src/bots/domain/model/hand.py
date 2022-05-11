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
    def create_relative_card(draw_id: DrawId, suit: Suit | None = None, rank: Rank | None = None) -> HandCard:
        if suit is not None and rank is not None:
            return HandCard(all_possible_cards(suit, rank), True, draw_id)
        elif suit is not None:
            return HandCard(all_possible_cards(suits=suit), True, draw_id)
        elif rank is not None:
            return HandCard(all_possible_cards(ranks=rank), True, draw_id)

        return HandCard(all_possible_cards(), False, draw_id)

    @staticmethod
    def create_real_card(draw_id: DrawId, card: Card, suit_known: bool = False, rank_known: bool = False) -> HandCard:
        if suit_known and rank_known:
            return HandCard(frozenset({card}), True, draw_id, real_card=card)
        elif suit_known:
            return HandCard(all_possible_cards(suits=card.suit), True, draw_id, real_card=card)
        elif rank_known:
            return HandCard(all_possible_cards(ranks=card.rank), True, draw_id, real_card=card)

        return HandCard(all_possible_cards(), False, draw_id, real_card=card)

    @staticmethod
    def known_real_card(draw_id: DrawId, card: Card) -> HandCard:
        return HandCard.create_real_card(draw_id, card, True, True)

    def __post_init__(self):
        self.notes_on_cards.update(self.possible_cards)

    def is_real(self, suit_or_rank: Suit | Rank) -> bool:
        return self.real_card is not None and self.real_card.matches(suit_or_rank)

    def __repr__(self):
        return f"{self.draw_id} -> {self.real_card if self.real_card is not None else self.possible_cards}"

    def is_known(self, suit_or_rank: Suit | Rank) -> bool:
        return all(card.matches(suit_or_rank) for card in self.possible_cards)

    @property
    def is_fully_known(self) -> bool:
        return len(self.notes_on_cards) == 1

    @property
    def fully_known_card(self) -> Card | None:
        if self.is_fully_known:
            return next(iter(self.notes_on_cards), None)


@dataclass(frozen=True)
class Hand(Iterable[HandCard], Sized):
    owner_name: str
    cards: tuple[HandCard, ...]

    @staticmethod
    def create_unknown_hand(player_name: str, size: int = 5) -> Hand:
        return Hand(player_name, tuple(HandCard.create_relative_card(0) for i in range(size)))

    @staticmethod
    def create_unknown_real_hand(player_name: str, cards: Iterable[Card]) -> Hand:
        return Hand(player_name, tuple(HandCard.create_real_card(0, card) for card in cards))

    def __iter__(self) -> Iterator[HandCard]:
        return iter(self.cards)

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, item) -> HandCard:
        return self.cards[item]

    def get_real(self, suit_or_rank: Suit | Rank) -> Iterable[tuple[Slot, HandCard]]:
        for slot, card in enumerate(self):
            if card.is_real(suit_or_rank):
                yield slot, card

    def __repr__(self):
        return f"{self.owner_name} {self.cards})"

    # FIXME this do not seem right... It this really a hand concern to update the interpretations?
    def add_interpretation(self, interpretation: dict[DrawId, set[Card]]):
        for card in self:
            if card.draw_id in interpretation:
                card.notes_on_cards.intersection_update(interpretation[card.draw_id])

    def find_card_by_draw_id(self, draw_id: DrawId) -> HandCard | None:
        for card in self:
            if card.draw_id == draw_id:
                return card

    def any_clued_could_be(self, card: Card) -> bool:
        return any(card in hand_card.notes_on_cards for hand_card in self if hand_card.is_clued)
