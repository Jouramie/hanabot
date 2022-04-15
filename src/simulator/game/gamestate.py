from dataclasses import dataclass
from typing import List, Dict
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

    def __init__(self, players: List[str]):
        self.currentTurn = 0
        self.currentClues = 8
        self.currentStrikes = 0
        self.actionHistory = []


    def can_play(self, card):
        stack = self.stacks[card.Suit]
        return stack.can_play(card)



