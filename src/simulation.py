import logging
import os
import time
from typing import List, Iterable

import plotext

from bots.machinabi.machinabi import Machinabi
from bots.ui.simulator import SimulatorBot
from core import Variant, Suit
from simulator.controller import Controller
from simulator.players.cheatingplayer import CheatingPlayer
from simulator.players.simulatorplayer import SimulatorPlayer


def play_game_slow(players: List[SimulatorPlayer], suits: Iterable[Suit], draw_game: bool = True, log_game: bool = False):
    controller = Controller(draw_game, log_game)
    game = controller.new_game(players, suits)
    controller.draw_game()
    while not controller.is_game_over():
        input("")
        controller.play_turn()
        controller.draw_game()


def play_games_fast(players: List[SimulatorPlayer], suits: Iterable[Suit], number_games: int, draw_game: bool = True, log_game: bool = False):
    controller = Controller(draw_game, log_game)
    total_score = 0
    total_survivals = 0
    total_victories = 0
    games_remaining = number_games
    time_before = time.time()
    results = []

    while games_remaining > 0:
        game = controller.new_game(players, suits)
        controller.try_play_until_game_is_over()
        result = controller.get_game_result()
        if not draw_game and games_remaining % 100 == 0:
            print(f"({number_games-games_remaining}/{number_games})")

        total_score = total_score + result.played_cards
        if result.is_survival:
            total_survivals = total_survivals + 1
        if result.is_victory:
            total_victories = total_victories + 1
        games_remaining = games_remaining - 1
        print_empty_lines(40)
        print_rates(total_survivals, total_victories, total_score, number_games - games_remaining)
        results.append(result)

    print_empty_lines(40)
    print_time_elapsed(number_games, time_before)
    print_rates(total_survivals, total_victories, total_score, number_games)

    possible_scores = list(range(0, 26))
    scores = {score: 0 for score in possible_scores}
    for result in results:
        scores[result.played_cards] = scores[result.played_cards] + 1
    plotext.bar(possible_scores, scores)
    plotext.title("Score Distribution")
    plotext.clc()
    plotext.show()


def print_empty_lines(number_lines: int):
    for i in range(0, number_lines):
        print("")


def print_time_elapsed(number_games: int, time_before: float):
    time_after = time.time()
    elapsed_seconds = time_after - time_before
    elapsed_seconds_rounded = round(elapsed_seconds, 3)
    elapsed_milliseconds = elapsed_seconds * 1000
    average_time_milliseconds_rounded = round(elapsed_milliseconds / number_games, 1)
    print(
        f"Finished simulating {str(number_games)} games in {str(elapsed_seconds_rounded)} seconds "
        f"(Average:{str(average_time_milliseconds_rounded)} ms per game)"
    )


def print_rates(total_survivals: int, total_victories: int, total_score: int, number_games: int):
    survival_rate = str(round(total_survivals / number_games * 100, 3))
    victory_rate = str(round(total_victories / number_games * 100, 3))
    average_score = str(round(total_score / number_games, 3))
    print("Survival Rate: " + survival_rate + "%")
    print("Victory Rate: " + victory_rate + "%")
    print("Average Score: " + average_score)


machinabi_players = [
    SimulatorBot("Alice", Machinabi()),
    SimulatorBot("Bob", Machinabi()),
    SimulatorBot("Cathy", Machinabi()),
    SimulatorBot("Donald", Machinabi()),
]
cheater_players = [
    CheatingPlayer(),
    CheatingPlayer(),
    CheatingPlayer(),
    CheatingPlayer(),
]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    clear = lambda: os.system("cls")
    simulation_players = cheater_players
    simulation_suits = Variant.NO_VARIANT

    print("Input 'Slow' to play one game slowly")
    print("Input 'Fast X' to play X games quickly")
    response = input().lower()
    words = response.split(" ")
    if response == "slow":
        play_game_slow(simulation_players, simulation_suits)
    elif words[0] == "fast" and len(words) == 2:
        play_games_fast(simulation_players, simulation_suits, int(words[1]), False)
    else:
        print("you suck at typing")
