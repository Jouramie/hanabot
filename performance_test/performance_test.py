import time

import pytest

from bots.hanabot import conventions
from bots.hanabot.hanabot import Hanabot
from bots.ui.simulator import SimulatorBot
from core import Variant
from simulator.controller import Controller

hanabot_players = [
    SimulatorBot("Alice", Hanabot(conventions.level_one)),
    SimulatorBot("Bob", Hanabot(conventions.level_one)),
    SimulatorBot("Cathy", Hanabot(conventions.level_one)),
    SimulatorBot("Donald", Hanabot(conventions.level_one)),
]


@pytest.mark.parametrize("number_games", [number_games for number_games in [1, 10, 100, 1000, 10000, 100000, 1000000]])
def test_hanabot_performance(number_games):
    time_before = time.time()

    controller = Controller(False, False)
    games_remaining = number_games
    results = []

    while games_remaining > 0:
        game = controller.new_game(hanabot_players, Variant.NO_VARIANT)
        controller.try_play_until_game_is_over()
        games_remaining = games_remaining - 1

    time_after = time.time()
    elapsed_seconds = time_after - time_before
    elapsed_seconds_rounded = round(elapsed_seconds, 3)
    elapsed_milliseconds = elapsed_seconds * 1000
    average_milliseconds = elapsed_milliseconds / number_games
    print("Played " + str(number_games) + " games in " + str(elapsed_milliseconds) + "ms (" + str(
        average_milliseconds) + "ms per game)")
