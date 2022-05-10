import logging
from typing import Dict, Tuple, List, Set

from bots.domain.decision import DecisionMaking, DiscardDecision, Decision, ClueDecision, SuitClueDecision, RankClueDecision
from bots.domain.model.action import ClueAction, RankClueAction, PlayAction
from bots.domain.model.game_state import RelativeGameState, GameHistory, Turn
from bots.domain.model.hand import Hand, DrawId, Slot
from bots.machinabi.analysed_clue import AnalysedClue
from bots.machinabi.potential_clue import PotentialClue
from core import Card, Rank

logger = logging.getLogger(__name__)


class Machinabi(DecisionMaking):
    potential_clues: List[PotentialClue]
    known_cards: Dict[DrawId, Card]
    analyzed_clues: List[AnalysedClue]
    last_analysed_turn: int
    cards_touched: Set[Card]
    cards_to_be_played: Set[Card]
    cards_maybe_touched: Set[Card]

    def __init__(self):
        self.new_game()

    def new_game(self):
        self.analyzed_clues = []
        self.last_analysed_turn = -1
        self.cards_touched = set()
        self.cards_to_be_played = set()
        self.cards_maybe_touched = set()

    def play_turn(self, current_game_state: RelativeGameState, history: GameHistory) -> Decision:
        self.analyze_turns_since_my_last_turn(history)

        if current_game_state.clue_count > 0:
            self.generate_all_potential_clues(current_game_state)
            self.remove_all_bad_potential_clues(current_game_state)

        if current_game_state.clue_count < 8:
            return self.discard_chop(current_game_state)

    def remove_all_bad_potential_clues(self, current_game_state: RelativeGameState):
        self.remove_all_bad_touch_potential_clues(current_game_state)
        self.remove_all_pointless_focus_potential_clues(current_game_state)

    def remove_all_bad_touch_potential_clues(self, current_game_state: RelativeGameState):
        for potential_clue in self.potential_clues:
            recipient_hand = current_game_state.player_hands[potential_clue.clue.receiver]
            cards_touched = self.get_all_new_cards_touched_by_potential_clue(recipient_hand, potential_clue.clue)
            for card_touched in cards_touched:
                if card_touched in self.cards_touched:
                    self.potential_clues.remove(potential_clue)

    def remove_all_pointless_focus_potential_clues(self, current_game_state: RelativeGameState):
        for potential_clue in self.potential_clues:
            recipient_hand = current_game_state.player_hands[potential_clue.clue.receiver]
            recipient_chop = self.get_player_chop_slot(recipient_hand)
            clue_focus = self.find_potential_clue_focus(recipient_hand, potential_clue.clue, recipient_chop)
            focused_card = recipient_hand[clue_focus]
            if not self.is_ready_to_play(current_game_state, focused_card.real_card)\
                    and not self.is_critical(focused_card.real_card):
                self.potential_clues.remove(potential_clue)

    def get_all_new_cards_touched_by_potential_clue(self, recipient_hand: Hand, clue: ClueDecision) -> set[Card]:
        cards_touched_by_clue = set()
        for card in recipient_hand:
            if card.is_clued:
                continue
            if isinstance(clue, SuitClueDecision) and clue.suit == card.real_card.suit:
                cards_touched_by_clue.add(card.real_card)
            if isinstance(clue, RankClueDecision) and clue.rank == card.real_card.rank:
                cards_touched_by_clue.add(card.real_card)
        return cards_touched_by_clue

    def get_all_slots_touched_by_potential_clue(self, recipient_hand: Hand, clue: ClueDecision) -> set[int]:
        slots_touched_by_clue = set()
        for slot in range(0, len(recipient_hand)):
            if isinstance(clue, SuitClueDecision) and clue.suit == recipient_hand[slot].real_card.suit:
                slots_touched_by_clue.add(slot)
            if isinstance(clue, RankClueDecision) and clue.rank == recipient_hand[slot].real_card.rank:
                slots_touched_by_clue.add(slot)
        return slots_touched_by_clue

    def analyze_turns_since_my_last_turn(self, history: GameHistory):
        for i in range(self.last_analysed_turn + 1, len(history.turns)):
            turn = history.turns[i]
            self.analyze_turn(turn)
        self.last_analysed_turn = len(history.turns) + 1

    def analyze_turn(self, turn: Turn):
        if isinstance(turn.action, PlayAction):
            return
        if isinstance(turn.action, DiscardDecision):
            return
        if isinstance(turn.action, ClueAction):
            self.analyzed_clues.append(self.analyze_given_clue(turn.game_state, turn.action))

    def analyze_given_clue(self, gamestate: RelativeGameState, clue: ClueAction) -> AnalysedClue:
        recipient_hand = gamestate.find_player_hand(clue.recipient)
        recipient_chop = self.get_player_chop_slot(recipient_hand)
        clue_focus = self.find_clue_focus(recipient_hand, clue.touched_slots, recipient_chop)
        if clue_focus == recipient_chop:
            is_save = self.chop_clue_is_save_clue(gamestate, clue)
            if is_save:
                return self.analyze_save_clue(recipient_hand, clue)

        return self.analyze_play_clue(recipient_hand, clue, clue_focus)

    def analyze_save_clue(self, recipient_hand: Hand, clue: ClueAction) -> AnalysedClue:
        for slot in clue.touched_slots:
            self.cards_touched.add(recipient_hand[slot].real_card)

        return AnalysedClue.save_clue()

    def analyze_play_clue(self, recipient_hand: Hand, clue: ClueAction, focus_slot: int) -> AnalysedClue:
        for slot in clue.touched_slots:
            self.cards_touched.add(recipient_hand[slot].real_card)
        self.cards_to_be_played.add(recipient_hand[focus_slot].real_card)
        return AnalysedClue.play_clue()

    def chop_clue_is_save_clue(self, gamestate: RelativeGameState, clue: ClueAction) -> bool:
        if isinstance(clue, RankClueAction):
            if clue.rank == Rank.FIVE:
                return True

        return False

    def find_potential_clue_focus(self, hand_before: Hand, clue: ClueDecision, chop_slot: Slot) -> Slot:
        touched_slots = self.get_all_slots_touched_by_potential_clue(hand_before, clue)
        return self.find_clue_focus(hand_before, touched_slots, chop_slot)

    def find_clue_focus(self, hand_before: Hand, touched_slots: Set[int], chop_slot: Slot) -> Slot:
        if chop_slot in touched_slots:
            return chop_slot

        newest_newly_touched_card_slot = 6
        for slot in touched_slots:
            if slot < newest_newly_touched_card_slot and not hand_before[slot].is_clued:
                newest_newly_touched_card_slot = slot

        return newest_newly_touched_card_slot

    def generate_all_potential_clues(self, current_game_state: RelativeGameState):
        potential_decisions = []
        for relative_position, player in enumerate(current_game_state.other_player_hands):
            for card in player.cards:
                rank_clue = RankClueDecision(card.real_card.rank, relative_position + 1)
                suit_clue = SuitClueDecision(card.real_card.suit, relative_position + 1)
                if rank_clue not in potential_decisions:
                    potential_decisions.append(rank_clue)
                if suit_clue not in potential_decisions:
                    potential_decisions.append(rank_clue)

        self.potential_clues = []
        for potential_decision in potential_decisions:
            self.potential_clues.append(PotentialClue(potential_decision))

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

    def is_critical(self, card: Card) -> bool:
        return card.rank == Rank.FIVE

    def is_ready_to_play(self, gamestate: RelativeGameState, card: Card) -> bool:
        if gamestate.stacks.is_already_played(card):
            return False

        for rank in [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE]:
            rank_card = Card(card.suit, rank)
            if gamestate.stacks.is_already_played(rank_card) or rank_card in self.cards_touched or rank_card in self.cards_to_be_played:
                continue
            if rank == card.rank:
                return True
            break

        return False


    def stall_clue(self, current_game_state: RelativeGameState):
        pass

    def anxiety_play(self, current_game_state: RelativeGameState):
        pass
