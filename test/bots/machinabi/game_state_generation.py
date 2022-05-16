from random import shuffle
from typing import List, Iterable, Tuple

from bots.domain.model.game_state import RelativeGameState, GameHistory
from bots.ui.simulator import add_recent_turns_to_history, assemble_relative_game_state
from core import Deck, Rank, Suit, Card
from simulator.game.game import Game
from test.simulator.game.game_setup import get_player_names


def get_game_random(number_players: int, suits: Iterable[Suit]) -> Game:
    game = Game(get_player_names(number_players), Deck.generate(suits))
    return game


def get_game_nothing_to_do(number_players: int, suits: Iterable[Suit]) -> Game:
    game = Game(get_player_names(number_players), Deck.starting_with(get_all_threes_and_fours(suits)))
    game.status.clues = 4
    return game


def get_game_all_possible_clues_are_single_touch(number_players: int) -> Game:
    cards_order = [
        Card(Suit.RED, Rank.ONE),
        Card(Suit.BLUE, Rank.ONE),
        Card(Suit.YELLOW, Rank.ONE),
        Card(Suit.GREEN, Rank.ONE),

        Card(Suit.BLUE, Rank.TWO),
        Card(Suit.YELLOW, Rank.TWO),
        Card(Suit.GREEN, Rank.TWO),
        Card(Suit.PURPLE, Rank.TWO),

        Card(Suit.YELLOW, Rank.THREE),
        Card(Suit.GREEN, Rank.THREE),
        Card(Suit.PURPLE, Rank.THREE),
        Card(Suit.RED, Rank.THREE),

        Card(Suit.GREEN, Rank.FOUR),
        Card(Suit.PURPLE, Rank.FOUR),
        Card(Suit.RED, Rank.FOUR),
        Card(Suit.BLUE, Rank.FOUR),

        Card(Suit.PURPLE, Rank.FIVE),
        Card(Suit.RED, Rank.FIVE),
        Card(Suit.BLUE, Rank.FIVE),
        Card(Suit.YELLOW, Rank.FIVE),
    ]
    game = Game(get_player_names(number_players), Deck.starting_with(cards_order))
    return game


def get_game_with_cards_in_order_in_starting_hands(number_players: int) -> Game:
    cards_order = [
        Card(Suit.RED, Rank.ONE),
        Card(Suit.BLUE, Rank.ONE),
        Card(Suit.GREEN, Rank.ONE),
        Card(Suit.YELLOW, Rank.ONE),

        Card(Suit.RED, Rank.ONE),
        Card(Suit.BLUE, Rank.ONE),
        Card(Suit.GREEN, Rank.ONE),
        Card(Suit.YELLOW, Rank.ONE),

        Card(Suit.RED, Rank.ONE),
        Card(Suit.BLUE, Rank.ONE),
        Card(Suit.GREEN, Rank.ONE),
        Card(Suit.YELLOW, Rank.ONE),

        Card(Suit.RED, Rank.TWO),
        Card(Suit.BLUE, Rank.TWO),
        Card(Suit.GREEN, Rank.TWO),
        Card(Suit.YELLOW, Rank.TWO),

        Card(Suit.RED, Rank.TWO),
        Card(Suit.BLUE, Rank.TWO),
        Card(Suit.GREEN, Rank.TWO),
        Card(Suit.YELLOW, Rank.TWO),

        Card(Suit.RED, Rank.THREE),
        Card(Suit.BLUE, Rank.THREE),
        Card(Suit.GREEN, Rank.THREE),
        Card(Suit.YELLOW, Rank.THREE),

        Card(Suit.RED, Rank.THREE),
        Card(Suit.BLUE, Rank.THREE),
        Card(Suit.GREEN, Rank.THREE),
        Card(Suit.YELLOW, Rank.THREE),

        Card(Suit.RED, Rank.FOUR),
        Card(Suit.BLUE, Rank.FOUR),
        Card(Suit.GREEN, Rank.FOUR),
        Card(Suit.YELLOW, Rank.FOUR),

        Card(Suit.RED, Rank.FOUR),
        Card(Suit.BLUE, Rank.FOUR),
        Card(Suit.GREEN, Rank.FOUR),
        Card(Suit.YELLOW, Rank.FOUR),

        Card(Suit.RED, Rank.FIVE),
        Card(Suit.BLUE, Rank.FIVE),
        Card(Suit.GREEN, Rank.FIVE),
        Card(Suit.YELLOW, Rank.FIVE),

        Card(Suit.PURPLE, Rank.ONE),
        Card(Suit.PURPLE, Rank.ONE),
        Card(Suit.PURPLE, Rank.ONE),
        Card(Suit.PURPLE, Rank.TWO),
        Card(Suit.PURPLE, Rank.TWO),
        Card(Suit.PURPLE, Rank.THREE),
        Card(Suit.PURPLE, Rank.THREE),
        Card(Suit.PURPLE, Rank.FOUR),
        Card(Suit.PURPLE, Rank.FOUR),
        Card(Suit.PURPLE, Rank.FIVE),
    ]
    game = Game(get_player_names(number_players), Deck.starting_with(cards_order))
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
    add_recent_turns_to_history(history, game, game.players[0].name, {})
    current_game_state = assemble_relative_game_state(game.current_state, game.current_player.name, {})
    return current_game_state, history
