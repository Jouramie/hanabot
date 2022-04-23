import logging
import os
import time
from typing import List, Iterable

from core import Variant, Suit
from simulator.controller import Controller
from simulator.game.gameresult import GameResult
from simulator.players.cheatingplayer import CheatingPlayer
from simulator.players.simulatorplayer import SimulatorPlayer


def print_game_result(result: GameResult):
    if result.is_victory:
        print("The team has won with a max score of " + str(result.score))
    elif result.is_survival:
        print("The team has survived with a score of " + str(result.score) + " out of " + str(result.max_score))
    else:
        print("The team has struck out after playing " + str(result.played_cards))


def play_game_slow(players: List[SimulatorPlayer], suits: Iterable[Suit]):
    controller = Controller()
    game = controller.new_game(players, suits)
    while not controller.is_game_over():
        controller.draw_game()
        input("")
        controller.play_turn()

    result = controller.get_game_result()
    print(result.final_state)
    print_game_result(result)


def play_games_fast(players: List[SimulatorPlayer], suits: Iterable[Suit], number_games: int):
    controller = Controller()
    total_score = 0
    total_survivals = 0
    total_victories = 0
    games_remaining = number_games
    time_before = time.time()
    while games_remaining > 0:
        game = controller.new_game(players, suits)
        controller.play_until_game_is_over()
        result = controller.get_game_result()
        print_game_result(result)

        total_score = total_score + result.played_cards
        if result.is_survival:
            total_survivals = total_survivals + 1
        if result.is_victory:
            total_victories = total_victories + 1
        games_remaining = games_remaining - 1

    time_after = time.time()
    elapsed_seconds = time_after - time_before
    elapsed_seconds_rounded = round(elapsed_seconds, 3)
    elapsed_milliseconds = elapsed_seconds * 1000
    average_time_milliseconds_rounded = round(elapsed_milliseconds / number_games, 1)

    print(
        f"Finished simulating {str(number_games)} games in {str(elapsed_seconds_rounded)} seconds "
        f"(Average:{str(average_time_milliseconds_rounded)} ms per game)"
    )

    print("Survival Rate: " + str(total_survivals / number_games * 100) + "%")
    print("Victory Rate: " + str(total_victories / number_games * 100) + "%")
    print("Average Score: " + str(total_score / number_games))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    clear = lambda: os.system("cls")
    players = [CheatingPlayer(), CheatingPlayer(), CheatingPlayer(), CheatingPlayer()]
    suits = Variant.NO_VARIANT

    print("Input 'Slow' to play one game slowly")
    print("Input 'Fast X' to play X games quickly")
    response = input().lower()
    words = response.split(" ")
    if response == "slow":
        play_game_slow(players, suits)
    elif words[0] == "fast" and len(words) == 2:
        play_games_fast(players, suits, int(words[1]))
    else:
        print("you suck at typing")
