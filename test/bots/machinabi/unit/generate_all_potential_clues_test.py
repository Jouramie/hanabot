import pytest

from bots.domain.model.game_state import RelativeGameState
from test.bots.machinabi.game_state_generation import assemble_relative_gamestate_and_history, \
    get_game_all_possible_clues_are_single_touch, get_game_with_cards_in_order_in_starting_hands
from bots.machinabi.machinabi import Machinabi
from core import Card, Suit, Rank, Variant
from core.stack import Stacks


def test_all_unique_cards():
    game = get_game_all_possible_clues_are_single_touch(4)
    relative_game, history = assemble_relative_gamestate_and_history(game)

    machinabi = Machinabi()

    machinabi.generate_all_potential_clues(relative_game)
    potential_clues = machinabi.potential_clues

    assert len(potential_clues) == 24


def test_very_few_clues():
    game = get_game_with_cards_in_order_in_starting_hands(4)
    relative_game, history = assemble_relative_gamestate_and_history(game)

    machinabi = Machinabi()

    machinabi.generate_all_potential_clues(relative_game)
    potential_clues = machinabi.potential_clues

    assert len(potential_clues) == 9
