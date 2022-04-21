import logging
from abc import ABC, abstractmethod
from threading import Thread
from time import sleep

from bots.domain.decision import DecisionMaking
from bots.domain.model.gamestate import GameState

logger = logging.getLogger(__name__)


class GameStateReader(ABC):
    @abstractmethod
    def see_current_state(self) -> GameState | None:
        pass


class GameStateReadingBot:
    def __init__(self, game_state_reader: GameStateReader, decision_making: DecisionMaking):
        self.game_state_reader = game_state_reader
        self.decision_making = decision_making
        self.stop_flag = False
        self.thread = Thread(target=self._bot_main_loop)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_flag = True

    def _bot_main_loop(self):
        """
        read game state
        reconsiliate player hand with history
        if current turn is bots
            bots.playturn

        sleep 100 ms
        """

        while True:
            if self.stop_flag:
                break

            try:
                current_state = self.game_state_reader.see_current_state()
                logger.info(current_state)

            except Exception as e:
                logger.exception(e)
            finally:
                sleep(0.1)
