from typing import Set

from bots.domain.decision import DecisionMaking, DecisionPlayAction, DecisionDiscardAction, DecisionSuitClueAction, DecisionRankClueAction
from bots.domain.model.gamestate import GameState, GameHistory
from bots.hanabot.convention import Convention


class Hanabot(DecisionMaking):
    def __init__(self, player_name: str, conventions: Set[Convention]):
        self.player_name = player_name
        self.conventions = conventions

    def play_turn(
        self, current_game_state: GameState, history: GameHistory
    ) -> DecisionPlayAction | DecisionDiscardAction | DecisionSuitClueAction | DecisionRankClueAction:
        """
        choose action (all hands + interpreted hands + stacks

        perform action

        """
        my_hand = current_game_state.get_player_hand(self.player_name)

        next_player_hand = current_game_state.get_next_player_hand(self.player_name)

        next_player_chop = next_player_hand.get_card_on_chop()

        # if current_game_state.is_critical(next_player_chop):

        # if possible card if playable or already played, play it (good touch principle)
        for card in my_hand:
            if current_game_state.stacks.are_all_playable_or_already_played(card.probable_cards):
                return DecisionPlayAction(card.slot)

        return DecisionDiscardAction(my_hand.get_card_on_chop().slot)
