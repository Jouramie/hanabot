from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Set

from bot.domain.model.clue import SuitClue, RankClue
from bot.domain.model.player import PlayerHand
from bot.domain.model.stack import Stacks
from core import Card


@dataclass(frozen=True)
class PlayAction:
    played_card: Card


@dataclass(frozen=True)
class DiscardAction:
    discarded_card: Card


@dataclass(frozen=True)
class ClueAction:
    recipient: str
    clue: SuitClue | RankClue


@dataclass(frozen=True)
class Turn:
    stacks: Stacks
    discard: Set[Card]
    hands: List[PlayerHand]
    last_performed_action: PlayAction | ClueAction | DiscardAction | None
    turnNumber: int
    clueCount: int
    bombCount: int


class GameStateReader(ABC):
    @abstractmethod
    def see_current_state(self) -> Turn | None:
        pass


@dataclass(frozen=True)
class GameHistory:
    game_states: List[Turn] = field(default_factory=list)

    def add_game_state(self, game_state: Turn) -> None:
        self.game_states.append(game_state)
