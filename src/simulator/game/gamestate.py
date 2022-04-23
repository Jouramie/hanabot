import logging
import random
from typing import List, Dict

from core import Deck, Card, Suit
from core.state.discard_pile import DiscardPile
from core.state.play_area import PlayArea
from core.state.status import Status
from core.gamerules import get_hand_size
from simulator.game.action import Action, PlayAction, ColorClueAction, RankClueAction, DiscardAction
from simulator.game.clue import ColorClue, RankClue, Clue
from simulator.game.hand_card import HandCard
from simulator.game.history import History
from simulator.game.player import Player
from core.state.stack import Stack

logger = logging.getLogger(__name__)


class GameState:
    players: List[Player]
    deck: Deck
    discard_pile: DiscardPile
    play_area: PlayArea
    history: History
    status: Status

    def __init__(self, players: List[str], deck: Deck):
        self.deck = deck
        self.discard_pile = DiscardPile()
        self.status = Status()
        self.history = History()
        self.play_area = PlayArea(deck.suits)

        self.players = []
        for playerName in players:
            self.players.append(Player(playerName))
        random.shuffle(self.players)

        number_of_players = len(self.players)
        for i in range(0, get_hand_size(number_of_players) * number_of_players):
            player_index = i % number_of_players
            self.player_draw_card(self.players[player_index])

        self.turns_remaining = number_of_players + self.deck.number_cards()

    @property
    def player_turn(self) -> int:
        return self.current_turn % len(self.players)

    def get_relative_player(self, relative_player_id: int) -> Player:
        return self.players[(self.player_turn + relative_player_id + 1) % len(self.players)]

    def player_draw_card(self, player: Player):
        if len(self.deck) == 0:
            return
        card = self.deck.draw()
        hand_card = HandCard(card, list(self.deck.variant.suits))
        player.hand.insert(0, hand_card)
        if len(self.deck) == 0:
            self.turns_remaining = len(self.players) + 1

    def next_turn(self):
        self.current_turn = self.current_turn + 1

    def add_strike(self):
        self.current_strikes = self.current_strikes + 1
        if self.current_strikes >= 3:
            self.is_over = True

    def play_turn(self, action: Action):
        action.actor = self.current_player

        action.act_on_state(self)

        self.next_turn()
        action.turn = self.current_turn

        self.action_history.append(action)
        self.turns_remaining = self.turns_remaining - 1
        if self.turns_remaining == 0:
            self.is_over = True

    def play_turn_play(self, action: PlayAction):
        player = self.current_player
        card_to_play = player.hand.pop(action.cardSlot)
        stack_to_play_on = self.stacks[card_to_play.real_card.suit]
        if stack_to_play_on.can_play(card_to_play.real_card):
            stack_to_play_on.play(card_to_play.real_card)
            action.success = True
        else:
            self.current_strikes = self.current_strikes + 1
            action.success = False
        self.player_draw_card(player)
        action.playedCard = card_to_play

    def play_turn_color_clue(self, action: ColorClueAction):
        clue = ColorClue(action.color, action.target_player.name, self.current_player.name, self.current_turn + 1)
        self.play_turn_clue(clue, action.target_player)

    def play_turn_rank_clue(self, action: RankClueAction):
        clue = RankClue(action.rank, action.target_player.name, self.current_player.name, self.current_turn + 1)
        self.play_turn_clue(clue, action.target_player)

    def play_turn_clue(self, clue: Clue, target_player: Player):
        self.current_clues = self.current_clues - 1
        for hand_card in target_player.hand:
            hand_card.receive_clue(clue)
        self.clue_history.append(clue)

    def play_turn_discard(self, action: DiscardAction):
        player = self.current_player
        if self.current_clues >= 8 or action.cardSlot < 0 or action.cardSlot >= len(player.hand):
            raise ValueError("Can't perform discard action")

        card_to_discard = player.hand.pop(action.cardSlot)
        self.discard_pile.append(card_to_discard.real_card)
        self.current_clues = self.current_clues + 1
        self.player_draw_card(player)
        action.discardedCard = card_to_discard.real_card

    @property
    def current_player(self):
        return self.players[self.player_turn]

    def get_player_by_name(self, name: str):
        for player in self.players:
            if player.name == name:
                return player

    def get_max_turns(self, number_players: int, number_suits: int) -> int:
        starting_clues = 8
        clues_per_discard = 1
        max_turns_per_deck_card = 1 + clues_per_discard
        total_cards = number_suits * 10
        hand_size = get_hand_size(number_players)
        cards_in_hands = hand_size * number_players
        deck_size = total_cards - cards_in_hands
        max_turns_from_emptying_deck = deck_size * max_turns_per_deck_card
        max_turns = max_turns_from_emptying_deck + number_players + starting_clues
        return max_turns
