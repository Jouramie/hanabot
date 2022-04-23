import logging
import random
from typing import List, Dict

from core.card import Card, Suit
from simulator.game.action import Action, PlayAction, ColorClueAction, RankClueAction, DiscardAction
from simulator.game.clue import ColorClue, RankClue
from simulator.game.deckgenerator import DeckGenerator
from simulator.game.gamerules import get_hand_size, get_max_turns
from simulator.game.hand_card import HandCard
from simulator.game.player import Player
from simulator.game.stack import Stack

logger = logging.getLogger(__name__)


class GameState:
    players: List[Player]
    action_history: List[Action]
    current_turn: int
    current_clues: int
    current_strikes: int
    deck: List[Card]
    discard_pile: List[Card]
    stacks: Dict[Suit, Stack]
    is_over: bool
    turns_remaining: int
    suits: List[Suit]

    def __init__(self, players: List[str], suits: List[Suit]):
        self.current_turn = 0
        self.current_clues = 8
        self.current_strikes = 0
        self.action_history = []
        self.is_over = False
        self.suits = suits

        generator = DeckGenerator()
        self.deck = generator.GenerateDeck(self.suits)
        self.discard_pile = []
        self.stacks = {}
        for suit in self.suits:
            self.stacks[suit] = Stack(suit)

        self.players = []
        for playerName in players:
            self.players.append(Player(playerName))
        random.shuffle(self.players)

        number_of_players = len(self.players)
        for i in range(0, get_hand_size(number_of_players) * number_of_players):
            player_index = i % number_of_players
            self.player_draw_card(self.players[player_index])

        self.turns_remaining = get_max_turns(number_of_players, len(self.suits))

    @property
    def player_turn(self) -> int:
        return self.current_turn % len(self.players)

    def get_relative_player(self, relative_player_id: int) -> Player:
        return self.players[(self.player_turn + relative_player_id + 1) % len(self.players)]

    def player_draw_card(self, player: Player):
        if len(self.deck) == 0:
            return
        card = self.deck.pop()
        hand_card = HandCard(card, self.suits)
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
        player = self.current_player
        clue = ColorClue(action.color, action.target_player.name, player.name, self.current_turn)
        self.current_clues = self.current_clues - 1
        # TODO: Actually handle the clue or something

    def play_turn_rank_clue(self, action: RankClueAction):
        player = self.current_player
        clue = RankClue(action.rank, action.target_player.name, player.name, self.current_turn)
        self.current_clues = self.current_clues - 1
        # TODO: Actually handle the clue or something

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
