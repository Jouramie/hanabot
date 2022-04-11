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


class PlayerBot:
    def bot_play_turn(self):
        """
        Algo:

        interpret hand (all clues + all hands + stacks)

        choose action (all hands + interpreted hands + stacks

        perform action

        """
        pass
