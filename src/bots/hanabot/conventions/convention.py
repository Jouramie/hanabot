from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Iterable

from bots.domain.decision import Decision, RankClueDecision, SuitClueDecision
from bots.domain.model.clue import Clue
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerHand, PlayerCard, RelativePlayerNumber, Slot
from core import Rank, Card


class InterpretationType(Enum):
    SAVE = auto()
    PLAY = auto()
    FIX = auto()


@dataclass(frozen=True)
class Interpretation:
    # TODO is the type really useful?
    interpretation_type: InterpretationType
    convention_name: str
    # TODO there probably is no override possible with fix clue
    possible_cards: dict[Slot, set[Card]]

    def __repr__(self) -> str:
        return f"{self.convention_name} {self.possible_cards})"


@dataclass(frozen=True)
class Convention(ABC):
    name: str

    @abstractmethod
    def find_play_clue(self, owner_slot_cards: tuple[RelativePlayerNumber, Slot, PlayerCard], current_game_state: RelativeGameState) -> Decision | None:
        pass

    @abstractmethod
    def find_interpretation(self, clue: Clue, current_game_state: RelativeGameState) -> Interpretation | None:
        pass


@dataclass(frozen=True)
class Conventions:
    conventions: Iterable[Convention]

    def find_save(self, card: PlayerCard, player_hand: PlayerHand) -> Decision:
        # TODO do better
        if card.real_card.rank == Rank.FIVE:
            return RankClueDecision(Rank.FIVE, player_hand.owner)

        if card.real_card.rank == Rank.TWO:
            return RankClueDecision(Rank.TWO, player_hand.owner)

        return SuitClueDecision(card.real_card.suit, player_hand.owner)

    def find_chop(self, player_hand: PlayerHand) -> int:
        # TODO that's not the chop lol
        return len(player_hand) - 1

    def find_card_on_chop(self, player_hand: PlayerHand) -> PlayerCard:
        return player_hand[self.find_chop(player_hand)]

    def find_play_clue(
        self, owner_slot_cards: Iterable[tuple[RelativePlayerNumber, Slot, PlayerCard]], current_game_state: RelativeGameState
    ) -> Iterable[Decision]:
        for owner_slot_card in owner_slot_cards:
            for convention in self.conventions:
                decision = convention.find_play_clue(owner_slot_card, current_game_state)
                if decision is not None:
                    yield decision

    @abstractmethod
    def find_interpretations(self, clue: Clue, current_game_state: RelativeGameState) -> list[Interpretation]:
        interpretations = []
        for convention in self.conventions:
            interpretation = convention.find_interpretation(clue, current_game_state)
            if interpretation is not None:
                interpretations.append(interpretation)

        return interpretations
