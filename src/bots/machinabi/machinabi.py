import logging
from typing import Dict, Tuple

from bots.domain.decision import DecisionMaking, DiscardDecision, Decision, ClueDecision, SuitClueDecision, RankClueDecision
from bots.domain.model.action import ClueAction, RankClueAction
from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.domain.model.hand import Hand, DrawId, Slot
from bots.machinabi.analysed_clue import AnalysedClue
from core import Card, Rank

logger = logging.getLogger(__name__)


class Machinabi(DecisionMaking):
    possible_clues: Dict[ClueDecision, float]
    known_cards: Dict[DrawId, Card]

    def __init__(self):
        pass

    def new_game(self):
        pass

    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        if current_game_state.clue_count > 0:
            self.evaluate_all_clues(current_game_state)
            best_clue, best_clue_value = self.find_best_clue()
            if best_clue_value >= 1:
                return best_clue

        if current_game_state.clue_count < 8:
            return self.discard_chop(current_game_state)
        pass

    def analyze_given_clue(self, gamestate: RelativeGameState, clue: ClueAction) -> AnalysedClue:
        recipient_hand = gamestate.find_player_hand(clue.recipient)
        recipient_chop = self.get_player_chop_slot(recipient_hand)
        clue_focus = self.find_clue_focus(recipient_hand, clue, recipient_chop)
        if clue_focus == recipient_chop:
            is_save = self.chop_clue_is_save_clue(gamestate, clue)
            if is_save:
                return AnalysedClue.save_clue()

        return AnalysedClue.play_clue()

    def chop_clue_is_save_clue(self, gamestate: RelativeGameState, clue: ClueAction) -> bool:
        if isinstance(clue, RankClueAction):
            if clue.rank == Rank.FIVE or clue.rank == Rank.TWO:
                return True

        return False

    def find_clue_focus(self, hand_before: Hand, clue: ClueAction, chop_slot: Slot) -> Slot:
        if chop_slot in clue.touched_slots:
            return chop_slot

        newest_newly_touched_card_slot = 6
        for slot in clue.touched_slots:
            if slot < newest_newly_touched_card_slot and not hand_before[slot].is_clued:
                newest_newly_touched_card_slot = slot

        return newest_newly_touched_card_slot

    def find_best_clue(self) -> Tuple[ClueDecision, float]:
        best_clue = None
        best_clue_value = -999999
        for clue, clue_value in self.possible_clues.items():
            if clue_value > best_clue_value:
                best_clue_value = clue_value
                best_clue = clue

        return best_clue, best_clue_value

    def evaluate_all_clues(self, current_game_state: RelativeGameState):
        self.possible_clues = {}
        for relative_position, player in enumerate(current_game_state.other_player_hands):
            for card in player.cards:
                is_critical = current_game_state.is_critical(card.real_card)
                is_playable = current_game_state.is_playable(card.real_card)
                if is_critical or is_playable:
                    rank_clue = RankClueDecision(card.real_card.rank, relative_position + 1)
                    suit_clue = SuitClueDecision(card.real_card.suit, relative_position + 1)
                    if rank_clue not in self.possible_clues:
                        self.possible_clues[rank_clue] = self.evaluate_clue_value(current_game_state, rank_clue)
                    if suit_clue not in self.possible_clues:
                        self.possible_clues[suit_clue] = self.evaluate_clue_value(current_game_state, suit_clue)

        return self.possible_clues

    def evaluate_clue_value(self, current_game_state: RelativeGameState, clue: ClueDecision) -> float:
        return 1

    def discard_chop(self, current_game_state: RelativeGameState) -> Decision:
        chop_slot = self.get_my_chop_slot(current_game_state)
        if -1 < chop_slot < len(current_game_state.my_hand):
            return DiscardDecision(chop_slot)

        return self.locked_hand_decision(current_game_state)

    def locked_hand_decision(self, current_game_state: RelativeGameState):
        if current_game_state.clue_count > 0:
            return self.stall_clue(current_game_state)
        return self.anxiety_play(current_game_state)

    def get_my_chop_slot(self, current_game_state: RelativeGameState) -> int:
        return self.get_player_chop_slot(current_game_state.my_hand)

    def get_player_chop_slot(self, player_hand: Hand) -> int:
        for slot in range(len(player_hand) - 1, -1, -1):
            if not player_hand[slot].is_clued:
                return slot

        return -1

    def stall_clue(self, current_game_state: RelativeGameState):
        pass

    def anxiety_play(self, current_game_state: RelativeGameState):
        pass
