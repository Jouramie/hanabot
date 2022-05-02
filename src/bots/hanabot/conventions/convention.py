from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from bots.domain.decision import Decision, RankClueDecision, SuitClueDecision
from bots.domain.model.action import Action
from bots.domain.model.game_state import RelativeGameState, RelativePlayerNumber
from bots.domain.model.hand import Hand, HandCard, Slot
from bots.hanabot.blackboard import Interpretation, Blackboard
from core import Rank


@dataclass(frozen=True)
class Convention(ABC):
    name: str

    @abstractmethod
    def find_play_clue(self, owner_slot_cards: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[Decision] | None:
        pass

    @abstractmethod
    def find_interpretation(self, action: Action, current_game_state: RelativeGameState) -> Interpretation | None:
        pass


@dataclass(frozen=True)
class Conventions:
    conventions: Iterable[Convention]

    def find_save(self, card: HandCard, player_hand: Hand) -> Decision:
        # TODO do better
        if card.real_card.rank == Rank.FIVE:
            return RankClueDecision(Rank.FIVE, player_hand.owner)

        if card.real_card.rank == Rank.TWO:
            return RankClueDecision(Rank.TWO, player_hand.owner)

        return SuitClueDecision(card.real_card.suit, player_hand.owner)

    def find_chop(self, hand: Hand) -> int | None:
        return next((slot for slot, card in list(enumerate(hand))[::-1] if not card.is_clued), None)

    def find_card_on_chop(self, player_hand: Hand) -> HandCard | None:
        chop = self.find_chop(player_hand)
        if chop is None:
            return None

        return player_hand[self.find_chop(player_hand)]

    def find_play_clue(
        self, owner_slot_cards: Iterable[tuple[RelativePlayerNumber, Slot, HandCard]], current_game_state: RelativeGameState
    ) -> Iterable[Decision]:
        for owner_slot_card in owner_slot_cards:
            for convention in self.conventions:
                decisions = convention.find_play_clue(owner_slot_card, current_game_state)
                if decisions is not None:
                    yield decisions[0]

    def find_new_interpretations(self, action: Action, blackboard: Blackboard) -> list[Interpretation]:
        interpretations = []
        for convention in self.conventions:
            # TODO should probably pass the game state at the time the clue was given
            interpretation = convention.find_interpretation(action, blackboard.current_game_state)
            if interpretation is not None:
                interpretations.append(interpretation)

        return interpretations
