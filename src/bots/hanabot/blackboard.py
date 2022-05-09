import logging
from dataclasses import dataclass, field
from enum import Enum, auto

from bots.domain.model.game_state import RelativeGameState, GameHistory, Turn
from bots.domain.model.hand import Slot, DrawId
from core import Card

logger = logging.getLogger(__name__)


class InterpretationType(Enum):
    SAVE = auto()
    PLAY = auto()
    FIX = auto()


@dataclass(frozen=True)
class Interpretation:
    of_turn: Turn
    focus: Slot | None = None
    # TODO is the type really useful?
    interpretation_type: InterpretationType | None = None
    explanation: str | None = None
    # TODO there probably is no override possible with fix clue
    notes_on_cards: dict[DrawId, set[Card]] = field(default_factory=dict)
    played_cards: set[DrawId] = field(default_factory=set)

    def __repr__(self) -> str:
        return f"{self.explanation} {self.notes_on_cards})"


@dataclass
class Blackboard:
    current_game_state: RelativeGameState | None = None
    history: GameHistory | None = None

    uninterpreted_turns: list[Turn] = field(default_factory=list)
    ongoing_interpretations: list[Interpretation] = field(default_factory=list)
    # TODO is this of any use?
    resolved_interpretations: list[Interpretation] = field(default_factory=list)

    def wipe_for_new_turn(self, current_game_state: RelativeGameState, history: GameHistory):
        if self.current_game_state is None:
            self.uninterpreted_turns = history.turns
        else:
            self.uninterpreted_turns = history.turns[self.current_game_state.turn_number :]

        self.current_game_state = current_game_state
        self.history = history

    def write_new_interpretation(self, interpretation: Interpretation):
        self.uninterpreted_turns.remove(interpretation.of_turn)
        self.ongoing_interpretations.append(interpretation)

    def write_notes_on_cards(self):
        for interpretation in self.ongoing_interpretations:
            for draw_id, cards in interpretation.notes_on_cards.items():
                hand_card = next((card for hand in self.current_game_state.player_hands for card in hand if card.draw_id == draw_id), None)
                if hand_card is not None:
                    hand_card.notes_on_cards.intersection_update(cards)

    def move_interpretation_to_resolved(self, interpretation: Interpretation):
        self.ongoing_interpretations.remove(interpretation)
        self.resolved_interpretations.append(interpretation)

    @property
    def my_hand(self):
        return self.current_game_state.my_hand
