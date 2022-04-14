from dataclasses import dataclass
from typing import List, Set

from bot.domain.card import Card, all_cards


@dataclass(frozen=True)
class PlayerCard:
    # Without interpretation, only basic clue information
    probableCards: Set[Card]
    handSlot: int
    drawnTurn: int


@dataclass(frozen=True)
class Hand:
    cards: List[PlayerCard]


def generate_unknown_hand() -> Hand:
    return Hand([PlayerCard(all_cards, i, 0) for i in range(5)])


@dataclass(frozen=True)
class Player:
    playerId: int
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
