from dataclasses import dataclass, field
from enum import Enum, auto

from bots.domain.model.action import Action
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.hand import Slot, DrawId
from core import Card


class InterpretationType(Enum):
    SAVE = auto()
    PLAY = auto()
    FIX = auto()


@dataclass(frozen=True)
class Interpretation:
    of_action: Action
    focus: Slot | None = None
    # TODO is the type really useful?
    interpretation_type: InterpretationType | None = None
    convention_name: str | None = None
    # TODO there probably is no override possible with fix clue
    possible_cards: dict[DrawId, set[Card]] = field(default_factory=dict)

    def __repr__(self) -> str:
        return f"{self.convention_name} {self.possible_cards})"


@dataclass
class Blackboard:
    current_game_state: RelativeGameState = None
    history: GameHistory = None

    chop: Slot | None = None

    uninterpreted_actions: list[Action] = field(default_factory=list)
    ongoing_interpretations: list[Interpretation] = field(default_factory=list)
    resolved_interpretations: list[Interpretation] = field(default_factory=list)

    @property
    def is_hand_locked(self):
        return self.chop is None
