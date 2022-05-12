from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Sized

from frozendict import frozendict

from core import Card, Rank

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Discard(Sized):
    discarded_cards: frozendict[Card, int] = field(default_factory=frozendict)

    def __len__(self) -> int:
        return sum(self.discarded_cards.values())

    def __contains__(self, card: Card) -> bool:
        return card in self.discarded_cards

    def __iter__(self) -> iter:
        return iter(self.discarded_cards)

    def count(self, card: Card) -> int:
        return self.discarded_cards.get(card, 0)

    def discard(self, card: Card) -> Discard:
        new_discard = Discard(self.discarded_cards.set(card, self.discarded_cards.get(card, 0) + 1))

        if card.rank is Rank.FIVE:
            logger.info("Good job everyone, a five going in the trash!")
        if card.number_of_copies == self.count(card):
            logger.info(f"Thanks to whoever thrown that {card}, the {card.suit} is screwed.")

        return new_discard

    def __repr__(self):
        return f"{dict(self.discarded_cards)}"
