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
    current_game_state: RelativeGameState | None = None
    history: GameHistory | None = None

    chop: Slot | None = None

    uninterpreted_actions: list[Action] = field(default_factory=list)
    ongoing_interpretations: list[Interpretation] = field(default_factory=list)
    resolved_interpretations: list[Interpretation] = field(default_factory=list)

    def wipe_for_new_turn(self, current_game_state: RelativeGameState, history: GameHistory):
        if self.current_game_state is None:
            self.uninterpreted_actions = history.action_history
        else:
            self.uninterpreted_actions = history.action_history[self.current_game_state.turn_number + 1 :]
        self.chop = None

        self.current_game_state = current_game_state
        self.history = history

    def write_new_interpretation(self, interpretation: Interpretation):
        self.uninterpreted_actions.remove(interpretation.of_action)
        self.ongoing_interpretations.append(interpretation)

    def write_notes_on_cards(self):
        for interpretation in self.ongoing_interpretations:
            for draw_id, cards in interpretation.possible_cards.items():
                hand_card = next((card for card in self.my_hand if card.draw_id == draw_id), None)
                if hand_card is not None:
                    hand_card.interpreted_cards.intersection_update(cards)

    @property
    def is_hand_locked(self):
        return self.chop is None

    @property
    def my_hand(self):
        return self.current_game_state.my_hand
