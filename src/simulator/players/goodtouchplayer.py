import logging
import random
from typing import List, Dict, Iterable

from core import Suit, Rank, Card
from core.card import default_distribution
from simulator.game.action import Action, PlayAction, RankClueAction, DiscardAction
from simulator.game.gamestate import GameState
from core.state.stack import Stack
from simulator.game.hand_card import HandCard
from simulator.players.simulatorplayer import SimulatorPlayer

logger = logging.getLogger(__name__)


class PossibleCard():
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
    def __init__(self):
        super().__init__("GoodTouchBot #" + str(random.randint(100, 1000)))

    def get_played_cards(self, game: GameState) -> List[Card]:
        played_cards = []
        for stack in game.play_area.stacks.values():
            for rank in stack.get_ranks_already_played():
                played_cards.append(Card(stack.suit, rank))

        return played_cards

    def play_turn(self, game: GameState) -> Action:
        maybe_touched_card = []
        touched_cards = self.get_played_cards(game)

        possible_hand = []
        for player in game.players:
            if player.name == self.name:
                for card in player.hand:
                    possible_hand.append(PossibleCard(game.deck.suits, card))
            else:
                for hand_card in player.hand:
                    if hand_card.is_clued:
                        touched_cards.append(hand_card.real_card)

        slots_i_can_play = {}
        for i in range(0, len(possible_hand)):
            possible_card = possible_hand[i]
            possibilities_to_remove = []
            for possibility in possible_card.possibilities:
                if possible_card.hand_card.get_all_possible_cards().count(possibility) < 1:
                    possibilities_to_remove.append(possibility)

            possible_card.remove_possibilities(possibilities_to_remove)
            if possible_card.hand_card.is_clued:
                possible_card.remove_possibilities(touched_cards)
                for possibility in possible_card.possibilities:
                    maybe_touched_card.append(possibility)

            can_play_for_sure = True
            lowest_rank_possible = 5
            for possibility in possible_card.possibilities:
                if not game.play_area.can_play(possibility):
                    can_play_for_sure = False
                    break;

                if possibility.rank.number_value < lowest_rank_possible:
                    lowest_rank_possible = possibility.rank.number_value

            if can_play_for_sure:
                slots_i_can_play[i] = lowest_rank_possible

        best_play_slot = -1
        best_play_rank = 5
        for slot, rank in slots_i_can_play.items():
            if rank <= best_play_rank:
                best_play_slot = slot
                best_play_rank = rank

        if best_play_slot > -1:
            return PlayAction(best_play_slot)

