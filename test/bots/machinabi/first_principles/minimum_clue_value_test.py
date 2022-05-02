import pytest

from bots.domain.decision import DiscardDecision, ClueDecision
from bots.machinabi.machinabi import Machinabi
from bots.ui.simulator import assemble_simulator_decision
from core import Variant
from simulator.game.gamestate import GameState
from test.bots.machinabi.game_state_generation import assemble_relative_gamestate_and_history, get_game_state_random


@pytest.mark.skip
@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_clue_should_always_have_value(number_players):
    gamestate = get_game_state_random(number_players, Variant.NO_VARIANT)

    players = []
    for i in range(0, number_players):
        players.append(Machinabi())

    chosen_decision = DiscardDecision(0)
    while not gamestate.status.is_over:
        relative_gamestate, history = assemble_relative_gamestate_and_history(gamestate)
        machinabi_to_play = players[gamestate.player_turn]
        chosen_decision = machinabi_to_play.play_turn(relative_gamestate, history)
        action = assemble_simulator_decision(chosen_decision, gamestate)

        cards_clued_before = count_clued_cards(gamestate)
        gamestate.play_turn(action)
        cards_clued_after = count_clued_cards(gamestate)

        if isinstance(chosen_decision, ClueDecision):
            assert cards_clued_after > cards_clued_before


def count_clued_cards(gamestate: GameState) -> int:
    total = 0
    for player in gamestate.players:
        for card in player.hand:
            if card.is_clued:
                total += 1

    return total