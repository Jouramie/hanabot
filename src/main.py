import logging
import signal
import sys
from time import sleep

from app.console import start_console_app
from context.hanabot_context import HanabotContext


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
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s", handlers=[logging.FileHandler("logs/hanabot.log", mode="w")])
    logging.getLogger("console").setLevel(logging.INFO)
    logger = logging.getLogger(__name__)

    start_console_app()
