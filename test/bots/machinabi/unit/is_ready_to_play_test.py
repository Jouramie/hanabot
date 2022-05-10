import pytest

from bots.domain.model.game_state import RelativeGameState
from test.bots.machinabi.game_state_generation import get_game_random, assemble_relative_gamestate_and_history
from bots.machinabi.machinabi import Machinabi
from core import Card, Suit, Rank, Variant
from core.stack import Stacks


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_one_is_ready_to_play_on_empty_stacks(number_players):
    game = get_game_random(number_players, Variant.NO_VARIANT)
    relative_game, history = assemble_relative_gamestate_and_history(game)

    card = Card(Suit.RED, Rank.ONE)

    machinabi = Machinabi()
    machinabi.cards_touched = set()
    machinabi.cards_maybe_touched = set()
    machinabi.cards_to_be_played = set()

    ready = machinabi.is_ready_to_play(relative_game, card)

    assert ready


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_one_is_not_ready_to_play_when_already_touched(number_players):
    game = get_game_random(number_players, Variant.NO_VARIANT)
    relative_game, history = assemble_relative_gamestate_and_history(game)

    card = Card(Suit.RED, Rank.ONE)

    machinabi = Machinabi()
    machinabi.cards_touched = set()
    machinabi.cards_touched.add(card)
    machinabi.cards_maybe_touched = set()
    machinabi.cards_to_be_played = set()

    ready = machinabi.is_ready_to_play(relative_game, card)

    assert not ready


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_two_is_not_ready_to_play_when_one_is_neither_played_nor_touched(number_players):
    game = get_game_random(number_players, Variant.NO_VARIANT)
    relative_game, history = assemble_relative_gamestate_and_history(game)

    card = Card(Suit.RED, Rank.TWO)

    machinabi = Machinabi()
    machinabi.cards_touched = set()
    machinabi.cards_maybe_touched = set()
    machinabi.cards_to_be_played = set()

    ready = machinabi.is_ready_to_play(relative_game, card)

    assert not ready


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_two_is_ready_to_play_when_one_is_played(number_players):
    game = get_game_random(number_players, Variant.NO_VARIANT)
    game.current_state, _ = game.current_state.play(Card(Suit.RED, Rank.ONE))
    relative_game, history = assemble_relative_gamestate_and_history(game)

    card = Card(Suit.RED, Rank.TWO)

    machinabi = Machinabi()
    machinabi.cards_touched = set()
    machinabi.cards_maybe_touched = set()
    machinabi.cards_to_be_played = set()

    ready = machinabi.is_ready_to_play(relative_game, card)

    assert ready


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_two_is_ready_to_play_when_one_is_touched(number_players):
    game = get_game_random(number_players, Variant.NO_VARIANT)
    relative_game, history = assemble_relative_gamestate_and_history(game)

    card = Card(Suit.RED, Rank.TWO)

    machinabi = Machinabi()
    machinabi.cards_touched = set()
    machinabi.cards_touched.add(Card(Suit.RED, Rank.ONE))
    machinabi.cards_maybe_touched = set()
    machinabi.cards_to_be_played = set()

    ready = machinabi.is_ready_to_play(relative_game, card)

    assert ready


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_two_is_not_ready_to_play_when_one_is_played_and_two_is_touched(number_players):
    game = get_game_random(number_players, Variant.NO_VARIANT)
    game.current_state, _ = game.current_state.play(Card(Suit.RED, Rank.ONE))
    relative_game, history = assemble_relative_gamestate_and_history(game)

    card = Card(Suit.RED, Rank.TWO)

    machinabi = Machinabi()
    machinabi.cards_touched = set()
    machinabi.cards_touched.add(Card(Suit.RED, Rank.TWO))
    machinabi.cards_maybe_touched = set()
    machinabi.cards_to_be_played = set()

    ready = machinabi.is_ready_to_play(relative_game, card)

    assert not ready


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_two_is_not_ready_to_play_when_one_and_two_are_touched(number_players):
    game = get_game_random(number_players, Variant.NO_VARIANT)
    relative_game, history = assemble_relative_gamestate_and_history(game)

    card = Card(Suit.RED, Rank.TWO)

    machinabi = Machinabi()
    machinabi.cards_touched = set()
    machinabi.cards_touched.add(Card(Suit.RED, Rank.ONE))
    machinabi.cards_touched.add(Card(Suit.RED, Rank.TWO))
    machinabi.cards_maybe_touched = set()
    machinabi.cards_to_be_played = set()

    ready = machinabi.is_ready_to_play(relative_game, card)

    assert not ready
