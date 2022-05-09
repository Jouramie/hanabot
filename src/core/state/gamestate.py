from __future__ import annotations

import logging
from copy import deepcopy
from typing import List

from core import Deck
from core.discard import Discard
from core.stack import Stacks
from core.state.status import Status
from simulator.game.player import Player
from util.profiling import timeit

logger = logging.getLogger(__name__)


class GameState:
    players: List[Player]
    deck: Deck
    discard_pile: Discard
    play_area: Stacks
    status: Status

    def __init__(self, players: List[Player], deck: Deck, discard_pile: Discard, play_area: Stacks, status: Status):
        self.players = players
        self.deck = deck
        self.discard_pile = discard_pile
        self.play_area = play_area
        self.status = status

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

    def discard(self, card) -> GameState:
        return GameState(self.players, self.deck, self.discard_pile.discard(card), self.play_area, self.status)

    def count_discarded(self, card) -> int:
        return self.discard_pile.count(card)

    def play(self, card) -> tuple[GameState, bool]:
        new_stacks, is_played = self.play_area.play(card)
        if not is_played:
            return self, False

        return GameState(self.players, self.deck, self.discard_pile, new_stacks, self.status), True

    @property
    def score(self) -> int:
        return self.play_area.stacks_score

    @timeit(name="Simulator.GameState.deepcopy")
    def __deepcopy__(self, memo):
        copy = GameState(
            deepcopy(self.players, memo),
            deepcopy(self.deck, memo),
            self.discard_pile,
            self.play_area,
            deepcopy(self.status, memo),
        )
        memo[id(self)] = copy
        return copy
