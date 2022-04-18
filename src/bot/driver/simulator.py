class SimulatedPlayer:
    """
    A simulated player that can be used to test the bot.
    """

    def __init__(self, name):
        self.name = name

    def get_move(self, board):
        """
        Gets the next move from the player.
        """
        return board.get_random_move()
