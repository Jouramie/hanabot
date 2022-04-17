from typing import List

from simulator.game.gamerules import get_hand_size
from simulator.game.gamestate import GameState
from simulator.game.player import Player
from test.simulator.game_setup import get_suits, get_player_names


def test_new_gamestate_should_have_8_clues():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert gamestate.current_clues == 8


def test_new_gamestate_should_be_on_turn_zero():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert gamestate.current_turn == 0


def test_new_gamestate_should_have_zero_strikes():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert gamestate.current_strikes == 0


def test_new_gamestate_should_not_be_over():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert not gamestate.is_over


def test_new_gamestate_should_have_empty_history():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert len(gamestate.action_history) == 0


def test_new_gamestate_should_have_empty_discard_pile():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert len(gamestate.discard_pile) == 0


def test_new_gamestate_should_be_first_players_turn():
    gamestate = GameState(get_player_names(5), get_suits(5))
    assert gamestate.player_turn == 0


def test_new_gamestate_2p_should_have_many_turns_remaining():
    number_players = 2
    number_suits = 5
    player_names = get_player_names(number_players)
    suits = get_suits(number_suits)
    gamestate = GameState(player_names, suits)
    assert gamestate.turns_remaining == get_max_turns(number_players, number_suits)


def test_new_gamestate_3p_should_have_many_turns_remaining():
    number_players = 3
    number_suits = 5
    player_names = get_player_names(number_players)
    suits = get_suits(number_suits)
    gamestate = GameState(player_names, suits)
    assert gamestate.turns_remaining == get_max_turns(number_players, number_suits)


def test_new_gamestate_4p_should_have_many_turns_remaining():
    number_players = 4
    number_suits = 5
    player_names = get_player_names(number_players)
    suits = get_suits(number_suits)
    gamestate = GameState(player_names, suits)
    assert gamestate.turns_remaining == get_max_turns(number_players, number_suits)


def test_new_gamestate_5p_should_have_many_turns_remaining():
    number_players = 5
    number_suits = 5
    player_names = get_player_names(number_players)
    suits = get_suits(number_suits)
    gamestate = GameState(player_names, suits)
    assert gamestate.turns_remaining == get_max_turns(number_players, number_suits)


def test_new_gamestate_6p_should_have_many_turns_remaining():
    number_players = 6
    number_suits = 5
    player_names = get_player_names(number_players)
    suits = get_suits(number_suits)
    gamestate = GameState(player_names, suits)
    assert gamestate.turns_remaining == get_max_turns(number_players, number_suits)


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


def test_new_gamestate_should_shuffle_6_players():
    player_names = get_player_names(6)
    gamestate1 = GameState(player_names, get_suits(5))
    gamestate2 = GameState(player_names, get_suits(5))
    players_are_different(gamestate1.players, gamestate2.players)


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
        assert stack.last_played is None


def test_new_gamestate_should_have_4_empty_stacks():
    suits = get_suits(4)
    gamestate = GameState(get_player_names(5), suits)
    assert len(gamestate.stacks) == len(suits)
    for stackSuit, stack in gamestate.stacks.items():
        assert stack.last_played is None


def test_new_gamestate_should_have_5_empty_stacks():
    suits = get_suits(5)
    gamestate = GameState(get_player_names(5), suits)
    assert len(gamestate.stacks) == len(suits)
    for stackSuit, stack in gamestate.stacks.items():
        assert stack.last_played is None


def test_new_gamestate_should_have_6_empty_stacks():
    suits = get_suits(6)
    gamestate = GameState(get_player_names(5), suits)
    assert len(gamestate.stacks) == len(suits)
    for stackSuit, stack in gamestate.stacks.items():
        assert stack.last_played is None


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
