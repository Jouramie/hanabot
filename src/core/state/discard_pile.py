import logging
from functools import reduce
from typing import List

from core import Card, Rank

logger = logging.getLogger(__name__)


class DiscardPile:
    cards: List[Card]

    def __init__(self):
        self.cards = []

    def discard(self, card: Card):
        self.cards.append(card)
        if card.rank is Rank.FIVE:
            logger.info("Good job everyone, a five going in the trash! 👏")
        if card.number_of_copies == reduce(lambda x, y: x + 1 if card == y else x, self.cards, 0):
            logger.info(f"Thanks to whoever thrown that {card}, the {card.suit} is screwed. 🎉")
