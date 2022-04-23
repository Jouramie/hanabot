from typing import Iterable

from core.card import Suit
from core.deck import Deck


class DeckGenerator:
    def generate_deck(self, suits: Iterable[Suit]) -> Deck:
        return Deck.generate(suits)
