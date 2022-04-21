from abc import ABC
from dataclasses import dataclass
from typing import Iterable

from bots.domain.decision import Decision, RankClueDecision, SuitClueDecision
from bots.domain.model.player import OtherPlayerCard, PlayerHand, PlayerCard
from core import Rank


class Convention(ABC):
    def __init__(self, name):
        self.name = name


@dataclass(frozen=True)
class Conventions:
    conventions: Iterable[Convention]

    def find_save(self, card: OtherPlayerCard, player_hand: PlayerHand) -> Decision:
        # TODO do better
        if card.real_card.rank == Rank.FIVE:
            return RankClueDecision(Rank.FIVE, player_hand.player_name)

        if card.real_card.rank == Rank.TWO:
            return RankClueDecision(Rank.TWO, player_hand.player_name)

        return SuitClueDecision(card.real_card.suit, player_hand.player_name)

    def find_card_on_chop(self, player_hand: PlayerHand) -> PlayerCard | OtherPlayerCard:
        """
        Finds the card on the chop
        :param player_hand: could be my hand or other player's hand
        :return: card on the chop
        """
        # TODO do better
        return player_hand.cards[-1]
