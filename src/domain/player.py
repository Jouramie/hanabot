from dataclasses import dataclass
from typing import List, Set

from domain.card import Card


@dataclass(frozen=True)
class PlayerCard:
    # Without interpretation, only basic clue information
    probableCards: Set[Card]
    handSlot: int
    drawnTurn: int


@dataclass(frozen=True)
class Hand:
    cards: List[PlayerCard]


@dataclass(frozen=True)
class Player:
    hand: Hand
