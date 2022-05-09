from bots.domain.decision import Decision, RankClueDecision
from bots.domain.model.action import RankClueAction
from bots.domain.model.game_state import RelativeGameState, RelativePlayerNumber, Turn
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

    def find_interpretation(self, turn: Turn) -> Interpretation | None:
        if not isinstance(turn.action, RankClueAction):
            return

        rank_clue = turn.action
        if rank_clue.rank != Rank.FIVE:
            return None

        touched_hand = turn.game_state.find_player_hand(rank_clue.recipient)
        chop = self.document.find_chop(touched_hand)
        focus = self.document.find_focus(rank_clue.touched_slots, touched_hand)
        if focus is not chop:
            return None

        return Interpretation(turn, interpretation_type=InterpretationType.SAVE, explanation=self.name)
