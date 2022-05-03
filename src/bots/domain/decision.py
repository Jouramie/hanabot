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


@dataclass(frozen=True)
class RankClueDecision:
    rank: Rank
    receiver: RelativePlayerNumber


Decision = PlayDecision | DiscardDecision | SuitClueDecision | RankClueDecision
ClueDecision = SuitClueDecision | RankClueDecision


class DecisionMaking(ABC):
    @abstractmethod
    def start_new_game(self):
        pass

    @abstractmethod
    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        pass
