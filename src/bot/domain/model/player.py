from dataclasses import dataclass
from typing import List, Iterable

from core import Card
from core.game_setup import all_possible_cards


@dataclass(frozen=True)
class PlayerCard:
    # Without interpretation, only basic clue information
    probableCards: Iterable[Card]
    handSlot: int
    drawnTurn: int


@dataclass(frozen=True)
class PlayerHand:
    playerName: str
    cards: List[PlayerCard]


def generate_unknown_hand() -> List[PlayerCard]:
    return [PlayerCard(all_possible_cards(), i, 0) for i in range(5)]
