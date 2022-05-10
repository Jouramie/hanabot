from dataclasses import dataclass

from bots.domain.model.hand import Slot, DrawId
from core import Card, Suit, Rank


@dataclass(frozen=True)
class PlayAction:
    draw_id: DrawId
    played_card: Card


@dataclass(frozen=True)
class DiscardAction:
    draw_id: DrawId
    discarded_card: Card


@dataclass(frozen=True)
class SuitClueAction:
    recipient: str
    touched_slots: frozenset[Slot]
    suit: Suit

    def __repr__(self):
        return f"{self.suit.name} on slots {set(self.touched_slots)}"

    def matches(self, card: Card) -> bool:
        return card.matches(self.suit)

    def __iter__(self):
        return iter(self.touched_slots)


@dataclass(frozen=True)
class RankClueAction:
    recipient: str
    touched_slots: frozenset[Slot]
    rank: Rank

    def __repr__(self):
        return f"{self.rank.name} on slots {set(self.touched_slots)}"

    def matches(self, card: Card) -> bool:
        return card.matches(self.rank)

    def __iter__(self):
        return iter(self.touched_slots)


ClueAction = SuitClueAction | RankClueAction
Action = PlayAction | DiscardAction | ClueAction
