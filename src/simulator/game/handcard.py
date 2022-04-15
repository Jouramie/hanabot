from dataclasses import dataclass
from enum import auto, Enum
from typing import List

from simulator.game.card import Card


@dataclass(frozen=True)
class HandCard:
    realCard: Card
    possibleCards: List[Card]

