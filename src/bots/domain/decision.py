from abc import ABC
from dataclasses import dataclass

from bots.domain.model.gamestate import GameState, GameHistory
from core import Suit, Rank


@dataclass(frozen=True)
class DecisionPlayAction:
    slot: int


@dataclass(frozen=True)
class DecisionDiscardAction:
    slot: int


@dataclass(frozen=True)
class DecisionSuitClueAction:
    suit: Suit
    player_name: str


@dataclass(frozen=True)
class DecisionRankClueAction:
    rank: Rank
    player_name: str


class DecisionMaking(ABC):
    def play_turn(
        self, current_game_state: GameState, history: GameHistory
    ) -> DecisionPlayAction | DecisionDiscardAction | DecisionSuitClueAction | DecisionRankClueAction:
        pass
