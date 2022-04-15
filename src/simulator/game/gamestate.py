from dataclasses import dataclass
from typing import List, Dict

from simulator.game.deckgenerator import DeckGenerator
from simulator.game.gamerules import get_hand_size
from simulator.game.stack import Stack
from simulator.game.action import Action
from simulator.game.card import Card, Suit
from simulator.game.player import Player


@dataclass
class GameState:
    players: List[Player]
    actionHistory: List[Action]
    currentTurn: int
    currentClues: int
    currentStrikes: int
    deck: List[Card]
    discardPile: List[Card]
    stacks: Dict[Suit, Stack]
    isOver: bool

    def __init__(self, players: List[str], suits: List[Suit]):
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
