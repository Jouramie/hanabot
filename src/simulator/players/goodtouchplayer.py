import logging
import random
from typing import List, Dict, Iterable, Tuple

from core import Suit, Rank, Card
from core.card import default_distribution
from core.state.play_area import PlayArea
from simulator.game.action import Action, PlayAction, RankClueAction, DiscardAction, ColorClueAction
from simulator.game.clue import ColorClue, Clue, RankClue
from core.state.gamestate import GameState
from simulator.game.hand_card import HandCard
from simulator.game.player import Player
from simulator.players.simulatorplayer import SimulatorPlayer

logger = logging.getLogger(__name__)


class PossibleCard:
    possibilities: List[Card]
    hand_card: HandCard

    def __init__(self, suits: Iterable[Suit], hand_card: HandCard):
        self.hand_card = hand_card
        self.possibilities = []
        for suit in suits:
            for rank in default_distribution.keys():
                self.possibilities.append(Card(suit, rank))

    def remove_possibilities(self, cards: Iterable[Card] | Card):
        if isinstance(cards, Card):
            cards = [cards]

        for card in cards:
            if self.possibilities.count(card) > 0:
                self.possibilities.remove(card)


class GoodTouchPlayer(SimulatorPlayer):
    cards_maybe_touched_in_my_hand: List[Card]
    cards_touched_visible: List[Card]
    myself: Player

    def __init__(self):
        super().__init__("GoodTouchBot #" + str(random.randint(100, 1000)))

    @staticmethod
    def get_played_cards(game: GameState) -> List[Card]:
        played_cards = []
        for stack in game.play_area.stacks.values():
            for rank in stack.get_ranks_already_played():
                played_cards.append(Card(stack.suit, rank))

        return played_cards

    def play_turn(self, game: GameState) -> Action:
        self.myself = game.current_player
        self.cards_maybe_touched_in_my_hand = []
        self.cards_touched_visible = self.get_played_cards(game)
        possible_hand = self.get_possibilities_from_hands(game)
        slots_i_can_play = self.get_slots_i_can_play(game, possible_hand)
        best_play_slot = self.choose_best_slot_to_play(slots_i_can_play)
        if best_play_slot > -1:
            return PlayAction(best_play_slot)

        best_clue = None
        best_clue_value = -100
        for player in game.players:
            if player.name == self.name:
                continue
            for rank in (Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE):
                best_clue, best_clue_value = self.evaluate_rank_clue_value(best_clue, best_clue_value, player, rank)
            for suit in game.deck.suits:
                best_clue, best_clue_value = self.evaluate_color_clue_value(best_clue, best_clue_value, player, suit)

        if game.status.clues > 0 and (best_clue_value >= 1 or game.status.clues >= 8):
            if best_clue is None:
                aaa = 5
            return best_clue

        for slot in range(len(self.myself.hand) - 1, -1, -1):
            if not self.myself.hand[slot].is_clued:
                return DiscardAction(slot)

        return DiscardAction(0)

    def evaluate_color_clue_value(self, best_clue: Action, best_clue_value: float, player: Player, suit: Suit)\
            -> Tuple[Action, float]:
        clue_action = ColorClueAction(suit, player)
        clue = ColorClue(suit, player.name, "", 0)
        return self.evaluate_clue_value(best_clue, best_clue_value, clue, clue_action, player.hand)

    def evaluate_rank_clue_value(self, best_clue: Action, best_clue_value: float, player: Player, rank: Rank)\
            -> Tuple[Action, float]:
        clue_action = RankClueAction(rank, player)
        clue = RankClue(rank, player.name, "", 0)
        return self.evaluate_clue_value(best_clue, best_clue_value, clue, clue_action, player.hand)

    def evaluate_clue_value(self, best_clue: Action, best_clue_value: float, clue: Clue, clue_action: Action,
                            player_hand: List[HandCard]) -> Tuple[Action, float]:
        value = 0
        for hand_card in player_hand:
            if clue.touches_card(hand_card.real_card):
                if hand_card.is_clued:
                    value += 0.2
                else:
                    if self.cards_touched_visible.count(hand_card.real_card) > 0:
                        value -= 10
                    elif self.cards_maybe_touched_in_my_hand.count(hand_card.real_card) > 0:
                        value -= 5
                    else:
                        value += 1
        if value > best_clue_value and value != 0:
            best_clue_value = value
            best_clue = clue_action
        return best_clue, best_clue_value

    def get_possibilities_from_hands(self, game: GameState) -> List[PossibleCard]:
        possible_hand = []
        for player in game.players:
            if player.name == self.name:
                for card in player.hand:
                    possible_hand.append(PossibleCard(game.deck.suits, card))
            else:
                for hand_card in player.hand:
                    if hand_card.is_clued:
                        self.cards_touched_visible.append(hand_card.real_card)
        return possible_hand

    def get_slots_i_can_play(self,
                             game: GameState,
                             possible_hand: list[PossibleCard]) -> Dict[int, int]:
        slots_i_can_play = {}
        cards_i_see_all_copies = self.get_cards_all_copies_visible(game)
        for i in range(0, len(possible_hand)):
            possible_card = possible_hand[i]
            self.remove_possibilities_from_clues(possible_card)
            self.remove_possibilities_from_touched_cards(possible_card)
            possible_card.remove_possibilities(cards_i_see_all_copies)
            can_play_for_sure, lowest_rank_possible = self.check_if_card_is_playable_for_sure(game.play_area, possible_card)

            if can_play_for_sure:
                slots_i_can_play[i] = lowest_rank_possible
        return slots_i_can_play

    @staticmethod
    def choose_best_slot_to_play(slots_i_can_play: Dict[int, int]) -> int:
        best_play_slot = -1
        best_play_rank = 5
        for slot, rank in slots_i_can_play.items():
            if rank <= best_play_rank:
                best_play_slot = slot
                best_play_rank = rank
        return best_play_slot

    @staticmethod
    def check_if_card_is_playable_for_sure(play_area: PlayArea, possible_card: PossibleCard) -> Tuple[bool, int]:
        can_play_for_sure = True
        lowest_rank_possible = 5
        for possibility in possible_card.possibilities:
            if not play_area.can_play(possibility):
                can_play_for_sure = False
                break

            if possibility.rank.number_value < lowest_rank_possible:
                lowest_rank_possible = possibility.rank.number_value
        return can_play_for_sure, lowest_rank_possible

    def remove_possibilities_from_touched_cards(self, possible_card: PossibleCard):
        if possible_card.hand_card.is_clued:
            possible_card.remove_possibilities(self.cards_touched_visible)
            for possibility in possible_card.possibilities:
                self.cards_maybe_touched_in_my_hand.append(possibility)

    @staticmethod
    def remove_possibilities_from_clues(possible_card: PossibleCard):
        possibilities_to_remove = []
        for possibility in possible_card.possibilities:
            if possible_card.hand_card.get_all_possible_cards().count(possibility) < 1:
                possibilities_to_remove.append(possibility)
        possible_card.remove_possibilities(possibilities_to_remove)

    def get_cards_all_copies_visible(self, game: GameState) -> List[Card]:
        card_numbers = {}
        for card in game.discard_pile.cards:
            if card not in card_numbers:
                card_numbers[card] = 0
            card_numbers[card] += 1

        for player in game.players:
            if player.name == self.myself.name:
                continue

            for hand_card in player.hand:
                if hand_card.real_card not in card_numbers:
                    card_numbers[hand_card.real_card] = 0
                card_numbers[hand_card.real_card] += 1

        for suit, stack in game.play_area.stacks.items():
            played_ranks = stack.get_ranks_already_played()
            for rank in played_ranks:
                card = Card(suit, rank)
                if card not in card_numbers:
                    card_numbers[card] = 0
                card_numbers[card] += 1

        cards_all_copies_visible = []
        for card, number in card_numbers.items():
            number_total = card.number_of_copies
            if number >= number_total:
                cards_all_copies_visible.append(card)

        return cards_all_copies_visible
