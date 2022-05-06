from random import shuffle
from typing import List, Iterable, Tuple

from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.ui.simulator import add_recent_turns_to_history
from core import Deck, Rank, Suit, Card
from simulator.game.game import Game
from test.simulator.game.game_setup import get_player_names


def get_game_random(number_players: int, suits: Iterable[Suit]):
    game = Game(get_player_names(number_players), Deck.generate(suits))
    return game


def get_game_nothing_to_do(number_players: int, suits: Iterable[Suit]):
    game = Game(get_player_names(number_players), Deck.starting_with(get_all_threes_and_fours(suits)))
    game.status.clues = 4
    return game


def get_all_threes_and_fours(suits: Iterable[Suit]) -> List[Card]:
    cards = []
    for suit in suits:
        cards.append(Card(suit, Rank.FOUR))
        cards.append(Card(suit, Rank.FOUR))
        cards.append(Card(suit, Rank.THREE))
        cards.append(Card(suit, Rank.THREE))

    shuffle(cards)
    return cards


def assemble_relative_gamestate_and_history(game: Game) -> Tuple[RelativeGameState, GameHistory]:
    history = GameHistory()
    add_recent_turns_to_history(history, game)
    return history[-1], history
