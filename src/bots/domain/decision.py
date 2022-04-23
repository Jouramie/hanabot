from abc import ABC
from dataclasses import dataclass

from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.player import RelativePlayerId
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
    receiver: RelativePlayerId


@dataclass(frozen=True)
class RankClueDecision:
    rank: Rank
    receiver: RelativePlayerId


Decision = PlayDecision | DiscardDecision | SuitClueDecision | RankClueDecision
ClueDecision = SuitClueDecision | RankClueDecision


class DecisionMaking(ABC):
    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        pass
