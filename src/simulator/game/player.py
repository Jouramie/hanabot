from dataclasses import dataclass
from typing import List
from simulator.game.handcard import HandCard


@dataclass(frozen=True)
class Player:
    name: str
    hand: List[HandCard]
