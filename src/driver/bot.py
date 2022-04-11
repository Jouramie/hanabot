from domain.game import GameStateReader


class Bot:
    def __init__(self, game_state_reader: GameStateReader):
        self.game_state_reader = game_state_reader
        pass

    def bot_thread_loop(self):
        """
        algo:
        read game state
        if current turn is bot
            bot.playturn

        sleep 100 ms
        """
        pass
