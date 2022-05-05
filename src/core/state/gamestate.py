from __future__ import annotations
import logging
import copy
from typing import List

from core import Deck
from core.state.discard_pile import DiscardPile
from core.state.play_area import PlayArea
from core.state.status import Status
from simulator.game.player import Player

logger = logging.getLogger(__name__)


class GameState:
    players: List[Player]
    deck: Deck
    discard_pile: DiscardPile
    play_area: PlayArea
    status: Status

    def __init__(self, players: List[Player], deck: Deck, discard_pile: DiscardPile, play_area: PlayArea, status: Status):
        self.players = copy.deepcopy(players)
        self.deck = copy.deepcopy(deck)
        self.discard_pile = copy.deepcopy(discard_pile)
        self.play_area = copy.deepcopy(play_area)
        self.status = copy.deepcopy(status)

    @staticmethod
    def from_gamestate(gamestate: GameState) -> GameState:
        return GameState(gamestate.players, gamestate.deck, gamestate.discard_pile, gamestate.play_area, gamestate.status)

    @property
    def player_turn(self) -> int:
        return self.status.turn % len(self.players)

    def get_relative_player(self, relative_player_id: int) -> Player:
        return self.players[(self.player_turn + relative_player_id) % len(self.players)]

    @property
    def current_player(self):
        return self.players[self.player_turn]

    def get_player_by_name(self, name: str):
        for player in self.players:
            if player.name == name:
                return player
