from dataclasses import dataclass
from typing import Iterable

from core import Card
from core.game_setup import all_possible_cards


@dataclass(frozen=True)
class PlayerCard:
    # Without interpretation, only basic clue information
    probable_cards: Iterable[Card]
    is_clued: bool
    slot: int
    drawn_turn: int


# TODO would it be simpler if this extend PlayerCard and Card?
@dataclass(frozen=True)
class OtherPlayerCard(PlayerCard):
    real_card: Card


@dataclass(frozen=True)
class PlayerHand:
    player_name: str
    cards: tuple[PlayerCard]

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, item):
        return self.cards[item]


def generate_unknown_hand() -> tuple[PlayerCard]:
    return tuple(PlayerCard(all_possible_cards(), False, i, 0) for i in range(5))
