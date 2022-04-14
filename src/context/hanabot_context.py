from driven.cv2.cv2_game_state_reader import Cv2GameStateReader, FromFileScreenshotter
from driver.bot import Bot


class HanabotContext:
    def start(self):
        self._initialize_context()
        self._actually_start()

    def _initialize_context(self):
        self.game_state_reader = Cv2GameStateReader(FromFileScreenshotter("test/resources/first-turn-my-turn.png"))
        self.bot = Bot(self.game_state_reader)

    def _actually_start(self):
        self.bot.start()

    def stop(self):
        self.bot.stop()
