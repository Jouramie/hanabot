from dataclasses import dataclass
from typing import Set

from bot.domain.convention import Convention
from bot.domain.model.turn import Turn, GameHistory, ClueAction, DiscardAction, PlayAction
from core import Suit, Rank


@dataclass(frozen=True)
class PlayerPlayAction:
    slot: int


@dataclass(frozen=True)
class PlayerDiscardAction:
    slot: int


@dataclass(frozen=True)
class PlayerSuitClueAction:
    suit: Suit
    player_name: str


@dataclass(frozen=True)
class PlayerRankClueAction:
    rank: Rank
    player_name: str


class Hanabot:
    def __init__(self, player_name: str, conventions: Set[Convention]):
        self.player_name = player_name
        self.conventions = conventions

    def play_turn(self, current_game_state: Turn, history: GameHistory) -> ClueAction | DiscardAction | PlayAction:
        """
        choose action (all hands + interpreted hands + stacks

        perform action

        """
        pass
