import logging
import sys
import time
from typing import List, Iterable

import console.detection
import console.utils
import plotext
from console.progress import ProgressBar

from bots.hanabot import conventions
from bots.hanabot.hanabot import Hanabot
from bots.machinabi.machinabi import Machinabi
from bots.ui.simulator import SimulatorBot
from core import Variant, Suit
from simulator.controller import Controller
from simulator.players.cheatingplayer import CheatingPlayer
from simulator.players.simulatorplayer import SimulatorPlayer

game_title = """
   Let's play       

  ██╗  ██╗ █████╗ ███╗   ██╗ █████╗ ██████╗ ██╗    ██╗
  ██║  ██║██╔══██╗████╗  ██║██╔══██╗██╔══██╗██║    ██║
  ███████║███████║██╔██╗ ██║███████║██████╔╝██║    ██║
  ██╔══██║██╔══██║██║╚██╗██║██╔══██║██╔══██╗██║    ╚═╝
  ██║  ██║██║  ██║██║ ╚████║██║  ██║██████╔╝██║    ██╗
  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝ ╚═╝    ╚═╝"""
player_selection_text = """Select your players:
  h  - Hanabot
  m  - Machinabi
  c  - Cheater"""
speed_selection_text = """
Input 'Slow' to play one game slowly
Input 'Fast X' to play X games quickly"""

players_names = {
    "h": "Hanabot",
    "m": "Machinabi",
    "c": "Cheater",
}

hanabot_players = [
    SimulatorBot("Alice", Hanabot(conventions.level_one)),
    SimulatorBot("Bob", Hanabot(conventions.level_one)),
    SimulatorBot("Cathy", Hanabot(conventions.level_one)),
    SimulatorBot("Donald", Hanabot(conventions.level_one)),
]
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


def play_game_slow(players: List[SimulatorPlayer], suits: Iterable[Suit], draw_game: bool = True, log_game: bool = False):
    controller = Controller(draw_game, log_game)
    game = controller.new_game(players, suits)
    controller.draw_game()
    while not controller.is_game_over():
        input()
        controller.play_turn()
        controller.draw_game()
    print("The game has ended. Press any key to continue.")


def play_games_fast(players: List[SimulatorPlayer], suits: Iterable[Suit], number_games: int, draw_game: bool = True, log_game: bool = False):
    controller = Controller(draw_game, log_game)
    total_score = 0
    total_survivals = 0
    total_victories = 0
    games_remaining = number_games
    time_before = time.time()
    results = []

    print(f"Running your {number_games} games...")
    while games_remaining > 0:
        game = controller.new_game(players, suits)
        controller.try_play_until_game_is_over()
        result = controller.get_game_result()

        total_score = total_score + result.played_cards
        if result.is_survival:
            total_survivals = total_survivals + 1
        if result.is_victory:
            total_victories = total_victories + 1
        games_remaining = games_remaining - 1
        print_progress(total_survivals, total_victories, total_score, number_games, games_remaining)
        results.append(result)

    print_time_elapsed(number_games, time_before)
    print_rates(total_survivals, total_victories, total_score, number_games)

    possible_scores = list(range(0, 26))
    scores = {score: 0 for score in possible_scores}
    for result in results:
        scores[result.played_cards] = scores[result.played_cards] + 1
    plotext.bar(possible_scores, scores)
    plotext.title("Score Distribution")
    console_size = console.detection.get_size()
    plotext.plotsize(width=80, height=console_size[1] - 5)
    plotext.clc()
    plotext.show()


def print_time_elapsed(number_games: int, time_before: float):
    time_after = time.time()
    elapsed_seconds = time_after - time_before
    elapsed_seconds_rounded = round(elapsed_seconds, 3)
    elapsed_milliseconds = elapsed_seconds * 1000
    average_time_milliseconds_rounded = round(elapsed_milliseconds / number_games, 1)
    print(
        console.utils.clear_lines(3),
        f"Finished simulating {str(number_games)} games in {str(elapsed_seconds_rounded)} seconds "
        f"(Average:{str(average_time_milliseconds_rounded)} ms per game)",
    )


def print_progress(total_survivals, total_victories, total_score, number_games, games_remaining):
    print(console.utils.clear_lines(3))
    bar = ProgressBar()
    print(bar(int((number_games - games_remaining) / number_games * 100)))
    print_rates(total_survivals, total_victories, total_score, number_games - games_remaining)
    pass


def print_rates(total_survivals: int, total_victories: int, total_score: int, number_games: int):
    survival_rate = str(round(total_survivals / number_games * 100, 3))
    victory_rate = str(round(total_victories / number_games * 100, 3))
    average_score = str(round(total_score / number_games, 3))

    print(f"Survival Rate: {survival_rate}%")
    print(f"Victory Rate: " + victory_rate + "%")
    print(f"Average Score: " + average_score)


def start_console_app():
    suits = Variant.NO_VARIANT

    with console.screen.Screen() as screen:

        with screen.location(0, 0):
            print(game_title)
        with screen.location(10, 0):
            print(player_selection_text)
            with screen.hidden_cursor():
                key = console.utils.wait_key()
                print(console.utils.clear_lines(3))

        if key == "h":
            players = hanabot_players
        elif key == "m":
            players = machinabi_players
        elif key == "c":
            players = cheater_players
        else:
            print("you suck at typing")
            input()
            sys.exit(0)
        with screen.location(10, 0):
            print(
                f"You will play with {players_names[key]}.",
                speed_selection_text,
            )

            response = input().lower()
            words = response.split(" ")
            if response == "slow":
                play_game_slow(players, suits, log_game=True)
            elif words[0] == "fast" and len(words) == 2:
                logging.root.setLevel(logging.WARNING)
                play_games_fast(players, suits, int(words[1]), draw_game=False, log_game=True)
            else:
                print("you suck at typing")
            with screen.hidden_cursor():
                console.utils.wait_key()
