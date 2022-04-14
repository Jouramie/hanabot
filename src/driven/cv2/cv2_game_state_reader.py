import cv2

from domain.game import GameStateReader, GameState


class Screenshotter:
    def screenshot(self):
        raise NotImplementedError


class FromFileScreenshotter(Screenshotter):
    def __init__(self, path):
        self.path = path

    def screenshot(self):
        return cv2.imread(self.path)


class Cv2GameStateReader(GameStateReader):
    def __init__(self, screenshotter: Screenshotter):
        self.screenshotter = screenshotter
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
        raise NotImplementedError
