from dataclasses import dataclass, field

from frozendict import frozendict

from core import Card


@dataclass(frozen=True)
class Discard:
    discarded_cards: frozendict[Card, int] = field(default_factory=frozendict)

    def __contains__(self, card: Card) -> bool:
        return card in self.discarded_cards

    def __iter__(self) -> iter:
        return iter(self.discarded_cards)

    def count(self, card: Card) -> int:
        return self.discarded_cards.get(card, 0)
