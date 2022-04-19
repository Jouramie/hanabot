from abc import ABC
from typing import List

from core.card import Card
from core.rank import Rank
from core.suit import Suit


class HandCard(ABC):

    def get_all_possible_cards(self) -> List[Card]:
        pass

    def get_all_possible_suits(self) -> List[Suit]:
        pass

    def get_all_possible_ranks(self) -> List[Rank]:
        pass
