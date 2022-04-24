from dataclasses import dataclass
from typing import List

from core.card import Card, Rank, Suit
from core.gamerules import get_suit_short_name


@dataclass
class Stack:
    suit: Suit
    last_played: Rank | None = None

    def __str__(self):
        stack_number = 0
        if self.last_played is not None:
            stack_number = self.last_played.number_value
        return get_suit_short_name(self.suit) + str(stack_number)

    def stack_score(self) -> int:
        if self.last_played is None:
            return 0
        return self.last_played.number_value

    def can_play(self, card: Card) -> bool:
        if card.suit != self.suit:
            return False
        if self.last_played is None:
            return card.rank == Rank.ONE
        return self.last_played.number_value == card.rank.number_value - 1

    def play(self, card: Card) -> bool:
        if self.can_play(card):
            self.last_played = card.rank
            return True
        return False

    def get_ranks_already_played(self) -> List[Rank]:
        ranks = []
        if self.last_played is None:
            return ranks
        ranks.append(Rank.ONE)
        if self.last_played == Rank.ONE:
            return ranks
        ranks.append(Rank.TWO)
        if self.last_played == Rank.TWO:
            return ranks
        ranks.append(Rank.THREE)
        if self.last_played == Rank.THREE:
            return ranks
        ranks.append(Rank.FOUR)
        if self.last_played == Rank.FOUR:
            return ranks
        ranks.append(Rank.FIVE)
        return ranks
