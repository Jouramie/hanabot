from random import shuffle
from typing import List, Iterable, Tuple

from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.ui.simulator import assemble_relative_gamestate, assemble_history
from core import Deck, Rank, Suit, Card
from test.simulator.game_setup import get_player_names
from simulator.game.gamestate import GameState


def get_game_state_nothing_to_do(number_players: int, suits: Iterable[Suit]):
    gamestate = GameState(get_player_names(number_players), Deck.starting_with(get_all_threes_and_fours(suits)))
    gamestate.status.clues = 4
    return gamestate


def get_all_threes_and_fours(suits: Iterable[Suit]) -> List[Card]:
    cards = []
    for suit in suits:
        cards.append(Card(suit, Rank.FOUR))
        cards.append(Card(suit, Rank.FOUR))
        cards.append(Card(suit, Rank.THREE))
        cards.append(Card(suit, Rank.THREE))

    shuffle(cards)
    return cards


def assemble_relative_gamestate_and_history(gamestate: GameState) -> Tuple[RelativeGameState, GameHistory]:
    return assemble_relative_gamestate(gamestate), assemble_history(gamestate)
