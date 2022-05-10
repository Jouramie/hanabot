import logging

from bots.domain.decision import Decision
from bots.domain.model.action import ClueAction
from bots.domain.model.game_state import RelativePlayerNumber, RelativeGameState, Turn
from bots.domain.model.hand import Slot, HandCard
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions.convention import Convention

logger = logging.getLogger(__name__)


class Prompt(Convention):
    def __init__(self):
        super().__init__("prompt")

    def find_clue(self, playable_card: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> list[Decision] | None:
        owner, slot, player_card = playable_card

        if not player_card.is_clued:
            return None

        next_card = player_card.real_card.next_card
        if next_card not in current_game_state.visible_cards:
            return None

        available_next_cards = current_game_state.find_hand_card(next_card)

        decisions = []
        for available_next_card in available_next_cards:
            decision = self.document.find_play_clue(available_next_card, current_game_state)
            if decision is None:
                continue
            logger.debug(f"{player_card} should also get played.")
            decisions.extend(decision)

        return decisions if len(decisions) > 0 else None

    def find_interpretation(self, turn: Turn) -> Interpretation | None:
        if not isinstance(turn.action, ClueAction) or len(turn.action.touched_slots) != 1:
            return

        clue = turn.action
        focus_card = self.find_focus_card(clue, turn.game_state.find_player_hand(clue.recipient))
        if focus_card is None:
            return

        if clue.recipient == turn.game_state.my_hand.owner_name:
            playable_cards = {card for card in focus_card.possible_cards if turn.game_state.is_playable_over_clued_playable(card)}

            if playable_cards:
                return Interpretation(
                    turn,
                    interpretation_type=InterpretationType.PLAY,
                    explanation=self.name,
                    notes_on_cards={focus_card.draw_id: set(playable_cards)},
                )
        else:
            if turn.game_state.is_playable(focus_card.real_card):
                return

            missing_cards_to_play = turn.game_state.find_missing_cards_to_play(focus_card.real_card)
            not_clued_missing_cards_to_play = [card for card in missing_cards_to_play if not turn.game_state.is_already_clued(card)]

            if not not_clued_missing_cards_to_play:
                return Interpretation(
                    turn,
                    interpretation_type=InterpretationType.PLAY,
                    explanation=self.name,
                    notes_on_cards={focus_card.draw_id: {focus_card.real_card}},
                )

            probable_missing_card = turn.game_state.my_hand.find_most_probable(not_clued_missing_cards_to_play)
            if len(not_clued_missing_cards_to_play) == len(probable_missing_card):
                return Interpretation(
                    turn,
                    interpretation_type=InterpretationType.PLAY,
                    explanation=self.name,
                    notes_on_cards={probable_missing_card[index].draw_id: {card} for index, card in enumerate(not_clued_missing_cards_to_play)},
                )

        return None
