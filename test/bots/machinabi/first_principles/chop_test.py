import pytest

from bots.domain.decision import DiscardDecision
from bots.machinabi.machinabi import Machinabi
from core import Variant
from simulator.game.clue import ColorClue
from test.bots.machinabi.game_state_generation import get_game_state_nothing_to_do, \
    assemble_relative_gamestate_and_history


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_nothing_to_do_should_discard_chop(number_players):
    gamestate = get_game_state_nothing_to_do(number_players, Variant.NO_VARIANT)
    gamestate.status.clues = 4
    relative_gamestate, history = assemble_relative_gamestate_and_history(gamestate)

    machinabi = Machinabi()
    chosen_decision = machinabi.play_turn(relative_gamestate, history)

    assert isinstance(chosen_decision, DiscardDecision)
    assert chosen_decision.slot == len(gamestate.players[0].hand) - 1


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_nothing_to_do_with_clued_cards_should_discard_chop(number_players):
    gamestate = get_game_state_nothing_to_do(number_players, Variant.NO_VARIANT)
    gamestate.status.clues = 4
    last_card = gamestate.current_player.hand[-1]
    last_card.receive_clue(ColorClue(last_card.real_card.suit, gamestate.current_player.name, "", 1))
    relative_gamestate, history = assemble_relative_gamestate_and_history(gamestate)

    machinabi = Machinabi()
    chosen_decision = machinabi.play_turn(relative_gamestate, history)

    assert isinstance(chosen_decision, DiscardDecision)
    assert chosen_decision.slot == len(gamestate.players[0].hand) - 2