import logging
from threading import Thread
from time import sleep

from domain.game import GameStateReader

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self, game_state_reader: GameStateReader):
        self.game_state_reader = game_state_reader
        self.stop_flag = False
        self.thread = Thread(target=self._bot_main_loop)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_flag = True

    def _bot_main_loop(self):
        """
        algo:
        read game state
        if current turn is bot
            bot.playturn

        sleep 100 ms
        """

        while True:
            if self.stop_flag:
                break

            try:
                current_state = self.game_state_reader.see_current_state()
                logger.info(current_state)

            except Exception as e:
                logger.error(repr(e))
            finally:
                sleep(0.1)
