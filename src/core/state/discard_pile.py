import logging
from typing import List

from core import Card, Rank

logger = logging.getLogger(__name__)


class DiscardPile:
    cards: List[Card]

    def __init__(self):
        self.cards = []

    def discard(self, card: Card):
        if card.rank is Rank.FIVE:
            logger.info("Good job everyone, a five going in the trash! 👏")
        self.cards.append(card)
