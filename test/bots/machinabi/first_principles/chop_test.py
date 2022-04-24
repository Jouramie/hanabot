# import pytest
#
# from bots.machinabi.machinabi import Machinabi
# from core import Variant
# from simulator.game.action import DiscardAction
# from test.bots.machinabi.game_state_generation import get_game_state_nothing_to_do
#
#
# @pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
# def test_nothing_to_do_should_discard_chop(number_players):
#     gamestate = get_game_state_nothing_to_do(number_players, Variant.NO_VARIANT)
#     gamestate.status.clues = 4
#     machinabi = Machinabi()
#     chosen_action = machinabi.play_turn(gamestate)
#
#     assert isinstance(chosen_action, DiscardAction)
#     assert chosen_action.cardSlot == len(gamestate.players[0].hand) - 1