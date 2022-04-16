import random

from dataclasses import dataclass
from typing import List, Dict

from simulator.game.deckgenerator import DeckGenerator
from simulator.game.gamerules import get_hand_size
from simulator.game.stack import Stack
from simulator.game.action import Action, PlayAction, ClueAction, DiscardAction
from simulator.game.card import Card, Suit
from simulator.game.player import Player


class GameState:
    players: List[Player]
    actionHistory: List[Action]
    playerTurn: int
    currentTurn: int
    currentClues: int
    currentStrikes: int
    deck: List[Card]
    discardPile: List[Card]
    stacks: Dict[Suit, Stack]
    isOver: bool

    def __init__(self, players: List[str], suits: List[Suit]):
        self.playerTurn = 0
        self.currentTurn = 0
        self.currentClues = 8
        self.currentStrikes = 0
        self.actionHistory = []
        self.isOver = False

        generator = DeckGenerator()
        self.deck = generator.GenerateDeck(suits)
        self.discardPile = []
        self.stacks = {}
        for suit in suits:
            self.stacks[suit] = Stack(suit)

        self.players = []
        for playerName in players:
            self.players.append(Player(playerName))
        random.shuffle(self.players)

        number_of_players = len(self.players)
        for i in range(0, get_hand_size(number_of_players) * number_of_players):
            player_index = i % number_of_players
            self.player_draw_card(self.players[player_index])

    def player_draw_card(self, player: Player):
        card = self.deck.pop()
        player.hand.append(card)

    def can_play(self, card):
        stack = self.stacks[card.Suit]
        return stack.can_play(card)

    def next_turn(self):
        self.playerTurn = (self.playerTurn + 1) % len(self.players)
        self.currentTurn = self.currentTurn + 1

    def add_strike(self):
        self.currentStrikes = self.currentStrikes + 1
        if self.currentStrikes >= 3:
            self.isOver = True

    def play_turn(self, action: Action):
        self.next_turn()
        action.actor = self.get_current_player()
        action.turn = self.currentTurn

        if action is PlayAction:
            self.play_turn_play(action)
        if action is ClueAction:
            self.play_turn_clue(action)
        if action is DiscardAction:
            self.play_turn_discard(action)

        self.actionHistory.append(action)

    def play_turn_play(self, action: PlayAction):
        player = self.get_current_player()
        card_to_play = player.hand.pop(action.cardSlot)
        stack_to_play_on = self.stacks[card_to_play.suit]
        if stack_to_play_on.can_play(card_to_play):
            stack_to_play_on.play(card_to_play)
            action.success = True
        else:
            self.currentStrikes = self.currentStrikes + 1
            action.success = False
        self.player_draw_card(player)
        action.playedCard = card_to_play

    def play_turn_clue(self, action: ClueAction):
        player = self.get_current_player()
        clue = action.clue
        clue.turn = self.currentTurn
        clue.giver = player
        # TODO: Actually handle the clue or something



    def play_turn_discard(self, action: DiscardAction):
        player = self.get_current_player()
        if self.currentClues >= 8 or action.cardSlot < 0 or action.cardSlot >= len(player.hand):
            raise ValueError('Can\'t perform discard action')

        card_to_discard = player.hand.pop(action.cardSlot)
        self.discardPile.append(card_to_discard)
        self.currentClues = self.currentClues + 1
        self.player_draw_card(player)
        action.discardedCard = card_to_discard

    def get_current_player(self):
        return self.players[self.playerTurn]
