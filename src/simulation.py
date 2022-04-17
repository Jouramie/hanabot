import os
import logging

from simulator.controller import Controller
from simulator.game.gameresult import GameResult
from simulator.game.suit import Suit
from simulator.players.cheatingplayer import CheatingPlayer


def print_game_result(result: GameResult):
    if result.is_victory:
        print("The team has won with a max score of " + str(result.score))
    elif result.is_survival:
        print("The team has survived with a score of " + str(result.score) + " out of " + str(result.max_score))
    else:
        print("The team has struck out after playing " + str(result.played_cards))


def play_game_slow():
    game = controller.new_game(players, suits)
    while not controller.is_game_over():
        controller.draw_game()
        input("")
        controller.play_turn()

    result = controller.get_game_result()
    print(result.final_state)
    print_game_result(result)


def play_games_fast(number_games: int):
    total_score = 0
    total_survivals = 0
    total_victories = 0
    games_remaining = number_games
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

    print("Survival Rate: " + str(total_survivals / number_games * 100) + "%")
    print("Victory Rate: " + str(total_victories / number_games * 100) + "%")
    print("Average Score: " + str(total_score / number_games))


logging.basicConfig(level=logging.INFO)

clear = lambda: os.system('cls')
controller = Controller()
players = [CheatingPlayer(), CheatingPlayer()]
suits = [Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW, Suit.PURPLE]

print("Input 'Slow' to play one game slowly")
print("Input 'Fast X' to play X games quickly")
response = input().lower()
words = response.split(" ")
if response == "slow":
    play_game_slow()
elif words[0] == "fast" and len(words) == 2:
    play_games_fast(int(words[1]))
else:
    print("you suck at typing")