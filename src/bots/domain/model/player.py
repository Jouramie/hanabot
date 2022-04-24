from dataclasses import dataclass, field
from typing import Iterable, Sized, Iterator, Type

from core import Card, Rank, Suit
from core.card import all_possible_cards

RelativePlayerNumber = int
Slot: Type[int] = int


@dataclass(frozen=True)
class PlayerCard:
    # Without interpretation, only basic clue information
    possible_cards: frozenset[Card]
    is_clued: bool
    drawn_turn: int
    real_card: Card | None = None
    interpreted_cards: set[Card] = field(default_factory=set)

    def __post_init__(self):
        self.interpreted_cards.update(self.possible_cards)

    def is_real(self, suit_or_rank: Suit | Rank) -> bool:
        return self.real_card is not None and self.real_card.matches(suit_or_rank)

    def __repr__(self):
        return f"{self.real_card if self.real_card is not None else self.possible_cards}"


@dataclass(frozen=True)
class PlayerHand(Iterable[PlayerCard], Sized):
    owner_name: str
    cards: tuple[PlayerCard, ...]

    def __iter__(self) -> Iterator[PlayerCard]:
        return iter(self.cards)

    def __len__(self) -> int:
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def get_real(self, suit_or_rank: Suit | Rank) -> Iterable[PlayerCard]:
        for card in self:
            if card.is_real(suit_or_rank):
                yield card

    def __repr__(self):
        return f"{self.owner_name} {self.cards})"

    # FIXME this do not seem right... It this really a hand concern to update the interpretations?
    def add_interpretation(self, interpretation: dict[Slot : set[Card]]):
        for slot, cards in interpretation.possible_cards.items():
            self.cards[slot].interpreted_cards.intersection_update(cards)


def create_unknown_card() -> PlayerCard:
    return PlayerCard(frozenset(all_possible_cards()), False, 0)


def create_unknown_real_card(card: Card) -> PlayerCard:
    return PlayerCard(frozenset(all_possible_cards()), False, 0, real_card=card)


def create_unknown_hand(player_name: str, size: int = 5) -> PlayerHand:
    return PlayerHand(player_name, tuple(create_unknown_card() for i in range(size)))


def create_unknown_real_hand(player_name: str, cards: Iterable[Card]) -> PlayerHand:
    return PlayerHand(player_name, tuple(create_unknown_real_card(card) for card in cards))


def create_known_real_card(card: Card) -> PlayerCard:
    return PlayerCard(frozenset({card}), True, 0, real_card=card)
