class GameStateReader:
    def __init__(self):
        self.first_turn = True

    def see_current_state(self):
        """
        algo:
        read state

        if first turn:
          left arrow
          if nothing changed
            return

        right arrow until nothing changes
        -> for each right arrow read state

        add all new state to history

        return global all states

        :return: multiple game states
        """
        pass
