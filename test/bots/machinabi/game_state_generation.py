from random import shuffle
from typing import List, Iterable

from core import Deck, Rank, Suit, Card, Variant
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
