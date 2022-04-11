from domain.game import GameState


class GameStateReader:
    def __init__(self):
        self.first_turn = True

    def see_current_state(self) -> GameState | None:
        """
        algo:

        if previous state is None
          previous state = read state()
          return previous state

        if previous state is first turn:
          left arrow
          previous state = read state()
          if nothing changed
            return None

        right arrow
        previous state = read state()
        if nothing changed
          return None

        return previous state
        """
        pass
