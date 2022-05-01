import logging

from bots.domain.decision import Decision
from bots.domain.model.action import Action, ClueAction
from bots.domain.model.game_state import RelativePlayerNumber, RelativeGameState
from bots.domain.model.hand import Slot, HandCard
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions.convention import Convention

logger = logging.getLogger(__name__)


class Prompt(Convention):
    def __init__(self):
        super().__init__("prompt")

    def find_play_clue(self, owner_slot_cards: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> Decision | None:
        pass

    def find_interpretation(self, action: Action, current_game_state: RelativeGameState) -> Interpretation | None:
        if not isinstance(action, ClueAction):
            return None

        if action.recipient == current_game_state.my_hand.owner_name:
            (touched_slot,) = action.touched_slots
            touched_card = current_game_state.my_hand[touched_slot]

            playable_cards = {card for card in touched_card.possible_cards if current_game_state.is_playable_over_clued_playable(card)}

            if playable_cards:
                logger.debug(f"{action} could be a {self.name}.")
                return Interpretation(
                    action, interpretation_type=InterpretationType.PLAY, convention_name=self.name, notes_on_cards={touched_card.draw_id: set(playable_cards)}
                )
        else:
            (touched_slot,) = action.touched_slots
            touched_card = current_game_state.find_player_hand(action.recipient)[touched_slot]

            if current_game_state.is_playable(touched_card.real_card):
                return None

            missing_cards_to_play = current_game_state.find_missing_cards_to_play(touched_card.real_card)
            not_clued_missing_cards_to_play = [card for card in missing_cards_to_play if not current_game_state.is_already_clued(card)]

            if not not_clued_missing_cards_to_play:
                logger.debug(f"{action} could be a {self.name}.")
                return Interpretation(
                    action,
                    interpretation_type=InterpretationType.PLAY,
                    convention_name=self.name,
                )

            probable_missing_card = current_game_state.my_hand.find_most_probable(not_clued_missing_cards_to_play)
            if len(not_clued_missing_cards_to_play) == len(probable_missing_card):
                logger.debug(f"{action} could be a {self.name}.")
                return Interpretation(
                    action,
                    interpretation_type=InterpretationType.PLAY,
                    convention_name=self.name,
                    notes_on_cards={probable_missing_card[index].draw_id: {card} for index, card in enumerate(not_clued_missing_cards_to_play)},
                )

        return None


class SelfPrompt(Convention):
    def find_play_clue(self, owner_slot_cards: tuple[RelativePlayerNumber, Slot, HandCard], current_game_state: RelativeGameState) -> Decision | None:
        pass

    def find_interpretation(self, action: Action, current_game_state: RelativeGameState) -> Interpretation | None:
        pass
