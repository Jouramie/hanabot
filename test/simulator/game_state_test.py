from typing import List

from simulator.game.gamestate import GameState
from test.simulator.game_setup import get_suits, get_player_names


def test_new_gamestate_should_have_8_clues():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert gamestate.currentClues == 8


def test_new_gamestate_should_be_on_turn_zero():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert gamestate.currentTurn == 0


def test_new_gamestate_should_have_zero_strikes():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert gamestate.currentStrikes == 0


def test_new_gamestate_should_not_be_over():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert not gamestate.isOver


def test_new_gamestate_should_have_empty_history():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert len(gamestate.actionHistory) == 0


def test_new_gamestate_should_have_empty_discard_pile():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert len(gamestate.discardPile) == 0


def test_new_gamestate_should_create_2_players():
    player_names = get_player_names(2)
    gamestate = GameState(player_names, get_suits(5))
    assert len(gamestate.players) == len(player_names)


def test_new_gamestate_should_create_3_players():
    player_names = get_player_names(3)
    gamestate = GameState(player_names, get_suits(5))
    assert len(gamestate.players) == len(player_names)


def test_new_gamestate_should_create_4_players():
    player_names = get_player_names(4)
    gamestate = GameState(player_names, get_suits(5))
    assert len(gamestate.players) == len(player_names)


def test_new_gamestate_should_create_5_players():
    player_names = get_player_names(5)
    gamestate = GameState(player_names, get_suits(5))
    assert len(gamestate.players) == len(player_names)


def test_new_gamestate_should_create_6_players():
    player_names = get_player_names(6)
    gamestate = GameState(player_names, get_suits(5))
    assert len(gamestate.players) == len(player_names)


def test_new_gamestate_should_give_cards_to_2_players():
    player_names = get_player_names(2)
    gamestate = GameState(player_names, get_suits(5))
    for player in gamestate.players:
        assert len(player.hand) == 5
    assert len(gamestate.deck) == 40


def test_new_gamestate_should_give_cards_to_3_players():
    player_names = get_player_names(3)
    gamestate = GameState(player_names, get_suits(5))
    for player in gamestate.players:
        assert len(player.hand) == 5
    assert len(gamestate.deck) == 35


def test_new_gamestate_should_give_cards_to_4_players():
    player_names = get_player_names(4)
    gamestate = GameState(player_names, get_suits(5))
    for player in gamestate.players:
        assert len(player.hand) == 4
    assert len(gamestate.deck) == 34


def test_new_gamestate_should_give_cards_to_5_players():
    player_names = get_player_names(5)
    gamestate = GameState(player_names, get_suits(5))
    for player in gamestate.players:
        assert len(player.hand) == 4
    assert len(gamestate.deck) == 30


def test_new_gamestate_should_give_cards_to_6_players():
    player_names = get_player_names(6)
    gamestate = GameState(player_names, get_suits(5))
    for player in gamestate.players:
        assert len(player.hand) == 3
    assert len(gamestate.deck) == 32


def test_new_gamestate_should_have_3_empty_stacks():
    suits = get_suits(3)
    gamestate = GameState(get_player_names(5), suits)
    assert len(gamestate.stacks) == len(suits)
    for stackSuit, stack in gamestate.stacks.items():
        assert stack.lastPlayed is None


def test_new_gamestate_should_have_4_empty_stacks():
    suits = get_suits(4)
    gamestate = GameState(get_player_names(5), suits)
    assert len(gamestate.stacks) == len(suits)
    for stackSuit, stack in gamestate.stacks.items():
        assert stack.lastPlayed is None


def test_new_gamestate_should_have_5_empty_stacks():
    suits = get_suits(5)
    gamestate = GameState(get_player_names(5), suits)
    assert len(gamestate.stacks) == len(suits)
    for stackSuit, stack in gamestate.stacks.items():
        assert stack.lastPlayed is None


def test_new_gamestate_should_have_6_empty_stacks():
    suits = get_suits(6)
    gamestate = GameState(get_player_names(5), suits)
    assert len(gamestate.stacks) == len(suits)
    for stackSuit, stack in gamestate.stacks.items():
        assert stack.lastPlayed is None
