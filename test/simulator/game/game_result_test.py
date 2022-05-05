import pytest

from core import Deck
from core.card import Rank, Suit
from simulator.game.game import Game
from simulator.game.gameresult import GameResult
from test.simulator.game.game_setup import get_player_names


def test_new_game_should_have_no_result():
    game = Game(get_player_names(5), Deck.generate())
    with pytest.raises(ValueError):
        GameResult.from_game_state(game.current_state)


def test_game_with_three_strikes_should_be_loss_result():
    game = Game(get_player_names(5), Deck.generate())
    game.play_area.stacks[Suit.RED].last_played = Rank.TWO
    game.status.add_strike()
    game.status.add_strike()
    game.status.add_strike()
    game_result = GameResult.from_game_state(game.current_state)
    assert not game_result.is_survival
    assert not game_result.is_victory
    assert game_result.score == 0
    assert game_result.played_cards == 2


def test_game_with_one_strike_should_be_result_with_score():
    game = Game(get_player_names(5), Deck.generate())
    game.play_area.stacks[Suit.RED].last_played = Rank.THREE
    game.play_area.stacks[Suit.BLUE].last_played = Rank.FIVE
    game.play_area.stacks[Suit.YELLOW].last_played = Rank.FOUR
    game.play_area.stacks[Suit.GREEN].last_played = Rank.FIVE
    game.play_area.stacks[Suit.PURPLE].last_played = Rank.FIVE
    game.status.add_strike()
    game.status.is_over = True
    game_result = GameResult.from_game_state(game.current_state)
    assert game_result.is_survival
    assert not game_result.is_victory
    assert game_result.score == 22
    assert game_result.played_cards == 22


def test_game_with_one_strike_should_be_victory_result_with_max_score():
    game = Game(get_player_names(5), Deck.generate())
    game.play_area.stacks[Suit.RED].last_played = Rank.FIVE
    game.play_area.stacks[Suit.BLUE].last_played = Rank.FIVE
    game.play_area.stacks[Suit.YELLOW].last_played = Rank.FIVE
    game.play_area.stacks[Suit.GREEN].last_played = Rank.FIVE
    game.play_area.stacks[Suit.PURPLE].last_played = Rank.FIVE
    game.status.add_strike()
    game.status.is_over = True
    game_result = GameResult.from_game_state(game.current_state)
    assert game_result.is_survival
    assert game_result.is_victory
    assert game_result.score == 25
    assert game_result.played_cards == 25
