import logging
import signal
import sys
from time import sleep

from app.console import start_console_app
from bots.hanabot import conventions
from bots.hanabot.hanabot import Hanabot
from bots.machinabi.machinabi import Machinabi
from bots.ui.simulator import SimulatorBot
from context.hanabot_context import HanabotContext
from simulator.players.cheatingplayer import CheatingPlayer


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


players_names = {
    "h": "Hanabot",
    "m": "Machinabi",
    "c": "CheatingPlayer",
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


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("console").setLevel(logging.INFO)
    logger = logging.getLogger(__name__)

    start_console_app()
