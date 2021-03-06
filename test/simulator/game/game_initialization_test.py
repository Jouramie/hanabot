from typing import List

import pytest

from core import Deck, Variant
from core.gamerules import get_hand_size
from simulator.game.game import Game
from simulator.game.player import Player
from test.simulator.game.game_setup import get_player_names


def test_new_game_should_have_8_clues():
    game = Game(get_player_names(5), Deck.generate())
    assert game.status.clues == 8


def test_new_game_should_be_on_turn_zero():
    game = Game(get_player_names(5), Deck.generate())
    assert game.status.turn == 0


def test_new_game_should_have_zero_strikes():
    game = Game(get_player_names(5), Deck.generate())
    assert game.status.strikes == 0


def test_new_game_should_not_be_over():
    game = Game(get_player_names(5), Deck.generate())
    assert not game.status.is_over


def test_new_game_should_have_empty_action_history():
    game = Game(get_player_names(5), Deck.generate())
    assert len(game.history.actions) == 0


def test_new_game_should_have_empty_clue_history():
    game = Game(get_player_names(5), Deck.generate())
    assert len(game.history.clues) == 0


def test_new_game_should_have_empty_discard_pile():
    game = Game(get_player_names(5), Deck.generate())
    assert len(game.current_state.discard_pile) == 0


def test_new_game_should_be_first_players_turn():
    game = Game(get_player_names(5), Deck.generate())
    assert game.player_turn == 0


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_new_game_should_have_many_turns_remaining(number_players):
    deck = Deck.generate()
    number_suits = len(deck.suits)
    player_names = get_player_names(number_players)
    game = Game(player_names, deck)
    assert game.status.turns_remaining == number_players + game.deck.number_cards()


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_new_game_should_create_players(number_players):
    player_names = get_player_names(number_players)
    game = Game(player_names, Deck.generate())
    assert len(game.players) == len(player_names)


def test_new_game_should_shuffle_6_players():
    player_names = get_player_names(6)
    game1 = Game(player_names, Deck.generate())
    game2 = Game(player_names, Deck.generate())
    players_are_different(game1.players, game2.players)


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_new_game_should_give_cards_to_all_players(number_players):
    player_names = get_player_names(number_players)
    game = Game(player_names, Deck.generate())
    expected_hand_size = get_hand_size(number_players)
    for player in game.players:
        assert len(player.hand) == expected_hand_size
    assert len(game.deck) == 50 - (expected_hand_size * number_players)


@pytest.mark.parametrize("number_suits", [number_suits for number_suits in range(3, 7)])
def test_new_game_should_have_empty_play_area(number_suits):
    suits = Variant.get_suits(number_suits)
    deck = Deck.generate(suits)
    game = Game(get_player_names(5), deck)
    assert len(game.current_state.play_area) == len(deck.suits)
    assert not game.current_state.play_area.played_cards


def players_are_different(players1: List[Player], players2: List[Player]):
    assert len(players1) == len(players2)
    for i in range(0, len(players1)):
        if players1[i].name != players2[i].name:
            return

    assert 0 == 1


def get_max_turns(number_players: int, number_suits: int) -> int:
    starting_clues = 8
    clues_per_discard = 1
    max_turns_per_deck_card = 1 + clues_per_discard
    total_cards = number_suits * 10
    hand_size = get_hand_size(number_players)
    cards_in_hands = hand_size * number_players
    deck_size = total_cards - cards_in_hands
    max_turns_from_emptying_deck = deck_size * max_turns_per_deck_card
    max_turns = max_turns_from_emptying_deck + number_players + starting_clues
    return max_turns
