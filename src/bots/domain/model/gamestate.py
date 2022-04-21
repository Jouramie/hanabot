from dataclasses import dataclass, field
from typing import List, Set

from bots.domain.model.clue import SuitClue, RankClue
from bots.domain.model.player import PlayerHand
from bots.domain.model.stack import Stacks
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
class GameState:
    stacks: Stacks
    discard: Set[Card]
    hands: List[PlayerHand]
    last_performed_action: PlayAction | ClueAction | DiscardAction | None
    turnNumber: int
    clueCount: int
    bombCount: int

    def get_player_hand(self, player_name: str) -> PlayerHand:
        return next(hand for hand in self.hands if hand.player_name == player_name)

    def get_next_player_hand(self, player_name: str) -> PlayerHand:
        return self.hands[(self.hands.index(self.get_player_hand(player_name)) + 1) % len(self.hands)]


@dataclass(frozen=True)
class GameHistory:
    game_states: List[GameState] = field(default_factory=list)

    def add_game_state(self, game_state: GameState) -> None:
        self.game_states.append(game_state)
