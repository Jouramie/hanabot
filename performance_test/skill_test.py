import pytest

from bots.hanabot import conventions
from bots.hanabot.hanabot import Hanabot
from bots.machinabi.machinabi import Machinabi
from bots.ui.simulator import SimulatorBot
from core import Variant
from simulator.controller import Controller

machinabi_players = [
    SimulatorBot("Alice", Machinabi()),
    SimulatorBot("Bob", Machinabi()),
    SimulatorBot("Cathy", Machinabi()),
    SimulatorBot("Donald", Machinabi()),
    SimulatorBot("Emily", Machinabi()),
    SimulatorBot("Frank", Machinabi()),
]

hanabot_players = [
    SimulatorBot("Alice", Hanabot(conventions.level_one)),
    SimulatorBot("Bob", Hanabot(conventions.level_one)),
    SimulatorBot("Cathy", Hanabot(conventions.level_one)),
    SimulatorBot("Donald", Hanabot(conventions.level_one)),
    SimulatorBot("Emily", Hanabot(conventions.level_one)),
    SimulatorBot("Frank", Hanabot(conventions.level_one)),
]

number_games = 100


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_machinabi_average_score(number_players):
    test_average_score(machinabi_players[0:number_players])


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_hanabot_average_score(number_players):
    test_average_score(hanabot_players[0:number_players])


@pytest.mark.skip()
def test_average_score(players):
    controller = Controller(False, False)
    games_remaining = number_games
    total_score = 0
    total_survivals = 0
    total_victories = 0

    while games_remaining > 0:
        game = controller.new_game(players, Variant.NO_VARIANT)
        controller.try_play_until_game_is_over()
        result = controller.get_game_result()

        total_score = total_score + result.played_cards
        if result.is_survival:
            total_survivals = total_survivals + 1
        if result.is_victory:
            total_victories = total_victories + 1
        games_remaining = games_remaining - 1

    print_rates(total_survivals, total_victories, total_score, number_games)


def print_rates(total_survivals: int, total_victories: int, total_score: int, number_games: int):
    survival_rate = str(round(total_survivals / number_games * 100, 3))
    victory_rate = str(round(total_victories / number_games * 100, 3))
    average_score = str(round(total_score / number_games, 3))

    print()
    print(f"Survival Rate: {survival_rate}%")
    print(f"Victory Rate: {victory_rate}%")
    print(f"Average Score: {average_score}")
