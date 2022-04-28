from abc import ABC
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
    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        pass
