from dataclasses import dataclass
from typing import List, Set

from bot.domain.model.card import Card, all_cards


@dataclass(frozen=True)
class PlayerCard:
    # Without interpretation, only basic clue information
    probableCards: Set[Card]
    handSlot: int
    drawnTurn: int


@dataclass(frozen=True)
class PlayerHand:
    playerName: str
    cards: List[PlayerCard]


def generate_unknown_hand() -> List[PlayerCard]:
    return [PlayerCard(all_cards, i, 0) for i in range(5)]
