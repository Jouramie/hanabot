from dataclasses import dataclass
from typing import List, Iterable

from core import Card
from core.game_setup import all_possible_cards


@dataclass(frozen=True)
class PlayerCard:
    # Without interpretation, only basic clue information
    probable_cards: Iterable[Card]
    is_clued: bool
    slot: int
    drawn_turn: int


@dataclass(frozen=True)
class PlayerHand:
    player_name: str
    cards: List[PlayerCard]

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, item):
        return self.cards[item]

    def get_card_on_chop(self):
        return self.cards[-1]


def generate_unknown_hand() -> List[PlayerCard]:
    return [PlayerCard(all_possible_cards(), False, i, 0) for i in range(5)]
