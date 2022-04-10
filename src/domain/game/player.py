from dataclasses import dataclass
from typing import List
from src.domain.game.card import Card


@dataclass(frozen=True)
class Player:
    name: str
    hand: List[Card]
