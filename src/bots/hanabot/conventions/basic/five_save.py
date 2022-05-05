from bots.domain.decision import Decision, RankClueDecision
from bots.domain.model.action import Action, RankClueAction
from bots.domain.model.game_state import RelativeGameState, RelativePlayerNumber
from bots.domain.model.hand import Slot, HandCard
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions.convention import Convention
from core import Rank


class FiveSave(Convention):
    def __init__(self):
        super().__init__("five save")

    def find_clue(self, card_to_clue: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[Decision] | None:
        relative_player_id, slot, card = card_to_clue
        if card.real_card.rank == Rank.FIVE:
            return [RankClueDecision(Rank.FIVE, relative_player_id)]

    def find_interpretation(self, action: Action, current_game_state: RelativeGameState) -> Interpretation | None:
        if isinstance(action, RankClueAction):
            # TODO validate clue was given on chop
            if action.rank == Rank.FIVE:
                return Interpretation(action, interpretation_type=InterpretationType.SAVE, explanation=self.name)
