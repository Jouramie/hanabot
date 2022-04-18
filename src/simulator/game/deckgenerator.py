from typing import List

from core import Suit, Card
from core.deck import generate


class DeckGenerator:
    def GenerateDeck(self, suits: List[Suit]) -> List[Card]:
        return generate(suits)
