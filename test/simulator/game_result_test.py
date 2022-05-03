import pytest

from core import Deck
from core.card import Rank, Suit
from simulator.game.gameresult import GameResult
from simulator.game.gamestate import GameState
from test.simulator.game_setup import get_player_names


def test_new_gamestate_should_have_no_result():
    gamestate = GameState(get_player_names(5), Deck.generate())
    with pytest.raises(ValueError):
        GameResult.from_game_state(gamestate)


def test_gamestate_with_three_strikes_should_be_loss_result():
    gamestate = GameState(get_player_names(5), Deck.generate())
    gamestate.play_area.stacks[Suit.RED].last_played = Rank.TWO
    gamestate.status.add_strike()
    gamestate.status.add_strike()
    gamestate.status.add_strike()
    game_result = GameResult.from_game_state(gamestate)
    assert not game_result.is_survival
    assert not game_result.is_victory
    assert game_result.score == 0
    assert game_result.played_cards == 2


def test_gamestate_with_one_strike_should_be_result_with_score():
    gamestate = GameState(get_player_names(5), Deck.generate())
    gamestate.play_area.stacks[Suit.RED].last_played = Rank.THREE
    gamestate.play_area.stacks[Suit.BLUE].last_played = Rank.FIVE
    gamestate.play_area.stacks[Suit.YELLOW].last_played = Rank.FOUR
    gamestate.play_area.stacks[Suit.GREEN].last_played = Rank.FIVE
    gamestate.play_area.stacks[Suit.PURPLE].last_played = Rank.FIVE
    gamestate.status.add_strike()
    gamestate.status.is_over = True
    game_result = GameResult.from_game_state(gamestate)
    assert game_result.is_survival
    assert not game_result.is_victory
    assert game_result.score == 22
    assert game_result.played_cards == 22


def test_gamestate_with_one_strike_should_be_victory_result_with_max_score():
    gamestate = GameState(get_player_names(5), Deck.generate())
    gamestate.play_area.stacks[Suit.RED].last_played = Rank.FIVE
    gamestate.play_area.stacks[Suit.BLUE].last_played = Rank.FIVE
    gamestate.play_area.stacks[Suit.YELLOW].last_played = Rank.FIVE
    gamestate.play_area.stacks[Suit.GREEN].last_played = Rank.FIVE
    gamestate.play_area.stacks[Suit.PURPLE].last_played = Rank.FIVE
    gamestate.status.add_strike()
    gamestate.status.is_over = True
    game_result = GameResult.from_game_state(gamestate)
    assert game_result.is_survival
    assert game_result.is_victory
    assert game_result.score == 25
    assert game_result.played_cards == 25
