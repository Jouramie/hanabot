import logging
from typing import Iterable

from bots.domain.decision import Decision
from bots.domain.model.action import ClueAction, SuitClueAction
from bots.domain.model.game_state import RelativePlayerNumber, Turn
from bots.domain.model.hand import Slot, HandCard, Hand, DrawId
from bots.hanabot.blackboard import Interpretation, InterpretationType, Blackboard
from bots.hanabot.conventions.convention import Convention
from core import Card

logger = logging.getLogger(__name__)


class Prompt(Convention):
    def __init__(self):
        super().__init__("prompt")

    def find_clue(self, playable_card: tuple[RelativePlayerNumber, Slot, HandCard], blackboard: Blackboard) -> list[Decision]:
        owner, slot, player_card = playable_card
        current_game_state = blackboard.current_game_state

        if not player_card.is_clued:
            return []

        next_card = player_card.real_or_fully_known_card.next_card
        if next_card is None or next_card not in current_game_state.visible_cards:
            return []

        available_next_cards = current_game_state.find_hand_card(next_card)

        decisions = []
        for available_next_card in available_next_cards:
            possible_decisions = self.document.find_play_clue(available_next_card, blackboard)
            if not possible_decisions:
                continue

            for decision in possible_decisions:
                action = blackboard.t0_action(decision)
                my_interpretations = self.find_interpretation(Turn(current_game_state, action, current_game_state))
                if not my_interpretations:
                    logger.debug(f"{decision} discarded, I don't even understand it...")
                    continue

                all_players_understand = True
                for relative_player_id, player in enumerate(current_game_state.player_hands, 1):
                    current_game_state_from_other_player_perspective = blackboard.from_player_perspective(relative_player_id)
                    other_player_interpretations = self.find_interpretation(
                        Turn(current_game_state_from_other_player_perspective, action, current_game_state_from_other_player_perspective)
                    )

                    if not other_player_interpretations or not my_interpretations.has_same_notes(other_player_interpretations):
                        logger.debug(f"{decision} discarded, {player.owner_name} would not understand.")
                        all_players_understand = False
                        break

                if not all_players_understand:
                    continue

                logger.debug(f"{player_card} should also get played.")
                decisions.extend(possible_decisions)

        return decisions if len(decisions) > 0 else None

    def find_interpretation(self, turn: Turn) -> Interpretation | None:
        if not isinstance(turn.action, ClueAction):
            return

        clue = turn.action
        focus_card = self.find_focus_card(clue, turn.previous_game_state.find_player_hand(clue.recipient))
        if focus_card is None:
            return

        if clue.recipient == turn.previous_game_state.my_hand.owner_name:
            return self.find_interpretation_for_clue_to_me(turn, focus_card)
        else:
            return self.find_interpretation_for_clue_to_others(turn, focus_card)

    def find_most_probables(self, cards: Iterable[Card], hand: Hand) -> list[HandCard] | None:
        most_probable = []
        for cards in cards:
            for hand_card in hand:
                if hand_card.is_clued and hand_card not in most_probable and (hand_card.is_known(cards.suit) or hand_card.is_known(cards.rank)):
                    most_probable.append(hand_card)

        if most_probable:
            return most_probable

    def find_interpretation_for_clue_to_others(self, turn: Turn, focus_card: HandCard) -> Interpretation | None:
        if turn.previous_game_state.is_playable(focus_card.real_card):
            return

        missing_cards_to_play = turn.previous_game_state.find_missing_cards_to_play(focus_card.real_card)
        not_clued_missing_cards_to_play = [card for card in missing_cards_to_play if not turn.previous_game_state.is_already_clued(card)]

        if not not_clued_missing_cards_to_play:
            visible_prompted_cards = [turn.previous_game_state.find_clued(card) for card in missing_cards_to_play]
            return Interpretation(
                turn,
                interpretation_type=InterpretationType.PLAY,
                explanation=self.name,
                notes_on_cards={
                    **{card.draw_id: {card.real_card} for clued_hand_cards in visible_prompted_cards for relative_player_id, slot, card in clued_hand_cards},
                    **{focus_card.draw_id: {focus_card.real_card}},
                },
            )

        not_clued_missing_cards_to_play.sort(key=lambda card: card.rank)
        probable_missing_card = self.find_most_probables(not_clued_missing_cards_to_play, turn.previous_game_state.my_hand)
        if probable_missing_card is None:
            return

        if len(not_clued_missing_cards_to_play) == len(probable_missing_card):
            return Interpretation(
                turn,
                interpretation_type=InterpretationType.PLAY,
                explanation=self.name,
                notes_on_cards={
                    **{probable_missing_card[index].draw_id: {card} for index, card in enumerate(not_clued_missing_cards_to_play)},
                    **{focus_card.draw_id: {focus_card.real_card}},
                },
            )

    def find_interpretation_for_clue_to_me(self, turn: Turn, focus_card: HandCard) -> Interpretation | None:
        if isinstance(turn.action, SuitClueAction):
            cards_leading_to: list[tuple[RelativePlayerNumber, DrawId, HandCard]] = []
            highest_possible_card: Card | None = None

            for card in reversed(turn.resulting_game_state.stacks.cards_left_to_play_on(turn.action.suit)):
                cards_leading_to = turn.resulting_game_state.find_clued_cards_leading_to(card)
                if cards_leading_to is not None:
                    highest_possible_card = card
                    break

            if not cards_leading_to or highest_possible_card is None:
                return

            return Interpretation(
                turn,
                interpretation_type=InterpretationType.PLAY,
                explanation=self.name,
                notes_on_cards={
                    **{card.draw_id: {card.real_or_fully_known_card} for _, _, card in cards_leading_to},
                    **{focus_card.draw_id: {highest_possible_card}},
                },
            )
