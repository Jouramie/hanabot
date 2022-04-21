from bots.infra.cv2.cv2_game_state_reader import Cv2GameStateReader, FromFileScreenshotter
from bots.ui.game_state_reading import GameStateReadingBot


class HanabotContext:
    def start(self):
        self._initialize_context()
        self._actually_start()

    def _initialize_context(self):
        self.game_state_reader = Cv2GameStateReader(FromFileScreenshotter("../test/resources/screenshots/first-turn-my-turn.png"))
        self.bot = GameStateReadingBot(self.game_state_reader)

    def _actually_start(self):
        self.bot.start()

    def stop(self):
        self.bot.stop()
