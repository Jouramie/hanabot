import pytest

from simulator.game.gameresult import GameResult
from simulator.game.gamestate import GameState
from test.simulator.game_setup import get_player_names, get_suits


def test_new_gamestate_should_have_no_result():
    gamestate = GameState(get_player_names(5), get_suits(5))
    with pytest.raises(ValueError):
        game_result = GameResult(gamestate)

