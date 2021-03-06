import pytest

from bots.domain.decision import DiscardDecision
from bots.machinabi.machinabi import Machinabi
from core import Variant
from simulator.game.clue import ColorClue
from test.bots.machinabi.game_state_generation import get_game_nothing_to_do, assemble_relative_gamestate_and_history


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_nothing_to_do_should_discard_chop(number_players):
    game = get_game_nothing_to_do(number_players, Variant.NO_VARIANT)
    game.status.clues = 4
    relative_game, history = assemble_relative_gamestate_and_history(game)

    machinabi = Machinabi()
    chosen_decision = machinabi.play_turn(relative_game, history)

    assert isinstance(chosen_decision, DiscardDecision)
    assert chosen_decision.slot == len(game.players[0].hand) - 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_nothing_to_do_with_last_card_clued_should_discard_second_last_as_chop(number_players):
    game = get_game_nothing_to_do(number_players, Variant.NO_VARIANT)
    game.status.clues = 4
    last_card = game.current_player.hand[-1]
    last_card.receive_clue(ColorClue(last_card.real_card.suit, game.current_player.name, "", 1))
    relative_game, history = assemble_relative_gamestate_and_history(game)

    machinabi = Machinabi()
    chosen_decision = machinabi.play_turn(relative_game, history)

    assert isinstance(chosen_decision, DiscardDecision)
    assert chosen_decision.slot == len(game.players[0].hand) - 2


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_nothing_to_do_with_two_last_card_clued_should_discard_third_last_as_chop(number_players):
    game = get_game_nothing_to_do(number_players, Variant.NO_VARIANT)
    game.status.clues = 4
    last_card = game.current_player.hand[-1]
    last_card.receive_clue(ColorClue(last_card.real_card.suit, game.current_player.name, "", 1))
    second_last_card = game.current_player.hand[-2]
    second_last_card.receive_clue(ColorClue(second_last_card.real_card.suit, game.current_player.name, "", 2))
    relative_game, history = assemble_relative_gamestate_and_history(game)

    machinabi = Machinabi()
    chosen_decision = machinabi.play_turn(relative_game, history)

    assert isinstance(chosen_decision, DiscardDecision)
    assert chosen_decision.slot == len(game.players[0].hand) - 3


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_nothing_to_do_with_locked_hand_should_not_discard(number_players):
    game = get_game_nothing_to_do(number_players, Variant.NO_VARIANT)
    game.status.clues = 4
    for card in game.current_player.hand:
        card.receive_clue(ColorClue(card.real_card.suit, game.current_player.name, "", 1))
    relative_game, history = assemble_relative_gamestate_and_history(game)

    machinabi = Machinabi()
    chosen_decision = machinabi.play_turn(relative_game, history)

    assert not isinstance(chosen_decision, DiscardDecision)