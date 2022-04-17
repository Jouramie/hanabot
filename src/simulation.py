import os
import logging

from simulator.controller import Controller
from simulator.game.suit import Suit
from simulator.players.cheatingplayer import CheatingPlayer


logging.basicConfig(level=logging.DEBUG)

clear = lambda: os.system('cls')
controller = Controller()
players = [CheatingPlayer(3), CheatingPlayer(3), CheatingPlayer(3), CheatingPlayer(3)]
suits = [Suit.BLUE, Suit.GREEN, Suit.RED, Suit.YELLOW, Suit.PURPLE]

game = controller.new_game(players, suits)
while not controller.is_game_over():
    controller.draw_game()
    input("")
    controller.play_turn()

result = controller.get_game_result()
print(result.final_state)
if result.is_victory:
    print("The team has won with a max score of " + str(result.score))
elif result.is_survival:
    print("The team has survived with a score of " + str(result.score) + " out of " + str(result.max_score))
else:
    print("The team has struck out after playing " + str(result.played_cards))
