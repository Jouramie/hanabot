import logging
import os
import signal
import sys
from time import sleep

from bots.hanabot import conventions
from bots.hanabot.hanabot import Hanabot
from bots.ui.simulator import SimulatorBot
from context.hanabot_context import HanabotContext
from core.card import Variant
from simulation import play_game_slow, play_games_fast
from simulator.controller import Controller


def bootstrap_reading_bot():
    global hanabot_context
    hanabot_context = HanabotContext()

    def signal_handler(signal, frame):
        logger.info("Exiting Hanabot.")
        hanabot_context.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    hanabot_context.start()
    while True:
        sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    clear = lambda: os.system("cls")
    controller = Controller()
    players = [
        SimulatorBot("Alice", Hanabot(conventions.basic)),
        SimulatorBot("Bob", Hanabot(conventions.basic)),
        SimulatorBot("Cathy", Hanabot(conventions.basic)),
        SimulatorBot("Donald", Hanabot(conventions.basic)),
    ]
    suits = Variant.NO_VARIANT

    print("Input 'Slow' to play one game slowly")
    print("Input 'Fast X' to play X games quickly")
    response = input().lower()
    words = response.split(" ")
    if response == "slow":
        play_game_slow(players, suits)
    elif words[0] == "fast" and len(words) == 2:
        play_games_fast(players, suits, int(words[1]), verbose=False)
    else:
        print("you suck at typing")
