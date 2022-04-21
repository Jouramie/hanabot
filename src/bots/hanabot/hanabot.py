from bots.domain.decision import DecisionMaking, PlayDecision, DiscardDecision, Decision
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.player import OtherPlayerCard
from bots.hanabot.convention import Conventions


class Hanabot(DecisionMaking):
    def __init__(self, player_name: str, conventions: Conventions):
        self.player_name = player_name
        self.conventions = conventions

    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        """
        choose action (all hands + interpreted hands + stacks

        perform action

        """
        my_hand = current_game_state.my_hand

        next_player_hand = current_game_state.other_player_hands[0]
        next_player_chop: OtherPlayerCard = self.conventions.find_card_on_chop(next_player_hand)

        if current_game_state.is_critical(next_player_chop.real_card):
            return self.conventions.find_save(next_player_chop, next_player_hand)

        current_game_state.find_not_clued_playable_cards()

        # if possible card if playable or already played, play it (good touch principle)
        for card in my_hand:
            if current_game_state.stacks.are_all_playable_or_already_played(card.probable_cards):
                return PlayDecision(card.slot)

        return DiscardDecision(self.conventions.find_card_on_chop(current_game_state.my_hand).slot)
