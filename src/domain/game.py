from dataclasses import dataclass


@dataclass(frozen=True)
class GameState:
    pass


class GameStateReader:
    def see_current_state(self) -> GameState | None:
        pass
