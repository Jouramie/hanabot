from dataclasses import dataclass
from typing import List, Set, Dict
from src.domain.game.stack import Stack
from src.domain.game.action import Action
from src.domain.game.card import Card, Suit
from src.domain.game.player import Player


@dataclass(frozen=True)
class GameState:
    players: List[Player]
    actionHistory: List[Action]
    currentTurn: int
    currentClues: int
    currentStrikes: int
    deck: List[Card]
    discardPile: List[Card]
    stacks: Dict[Suit, Stack]

    def can_play(self, card):
        stack = self.stacks[card.Suit]
        return stack.can_play(card)



