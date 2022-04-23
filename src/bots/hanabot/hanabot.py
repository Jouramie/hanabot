from bots.domain.decision import DecisionMaking, PlayDecision, DiscardDecision, Decision, SuitClueDecision
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.hanabot.conventions.convention import Conventions


SAVE_CLUE_ENABLED = False


class Hanabot(DecisionMaking):
    def __init__(self, conventions: Conventions):
        self.conventions = conventions

    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        """
        choose action (all hands + interpreted hands + stacks

        perform action

        """
        next_player_hand = current_game_state.other_player_hands[0]
        next_player_chop = self.conventions.find_card_on_chop(next_player_hand)

        if SAVE_CLUE_ENABLED and current_game_state.can_give_clue() and current_game_state.is_critical(next_player_chop.real_card):
            return self.conventions.find_save(next_player_chop, next_player_hand)

        # if possible card if playable or already played, play it (good touch principle)
        for slot, card in enumerate(current_game_state.my_hand):
            if current_game_state.stacks.are_all_playable_or_already_played(card.probable_cards):
                return PlayDecision(slot)

        if current_game_state.can_give_clue():
            owner_slot_cards = current_game_state.find_playable_cards()
            for possible_decision in self.conventions.find_play_clue(owner_slot_cards, current_game_state):
                return possible_decision

        if current_game_state.can_discard():
            return DiscardDecision(self.conventions.find_chop(current_game_state.my_hand))

        # Waste clue
        return SuitClueDecision(next_player_hand[0].real_card.suit, 1)
