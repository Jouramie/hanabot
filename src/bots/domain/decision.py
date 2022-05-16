from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from bots.domain.model.game_state import RelativeGameState, GameHistory, RelativePlayerNumber
from core import Suit, Rank


@dataclass(frozen=True)
class PlayDecision:
    slot: int


@dataclass(frozen=True)
class DiscardDecision:
    slot: int


@dataclass(frozen=True)
class SuitClueDecision:
    suit: Suit
    receiver: RelativePlayerNumber

    def __eq__(self, other: SuitClueDecision):
        if not isinstance(other, SuitClueDecision):
            return False
        return self.suit == other.suit and self.receiver == other.receiver


@dataclass(frozen=True)
class RankClueDecision:
    rank: Rank
    receiver: RelativePlayerNumber

    def __eq__(self, other: ClueDecision):
        if not isinstance(other, RankClueDecision):
            return False
        return self.rank == other.rank and self.receiver == other.receiver


Decision = PlayDecision | DiscardDecision | SuitClueDecision | RankClueDecision
ClueDecision = SuitClueDecision | RankClueDecision


class DecisionMaking(ABC):
    @abstractmethod
    def new_game(self):
        pass

    @abstractmethod
    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        pass
