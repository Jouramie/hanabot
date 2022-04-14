import logging
import signal
import sys
from time import sleep

from context.hanabot_context import HanabotContext

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    hanabot_context = HanabotContext()

    def signal_handler(signal, frame):
        logger.info("Exiting Hanabot.")
        hanabot_context.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    hanabot_context.start()

    while True:
        sleep(1)
