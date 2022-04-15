from simulator.game.action import Action
from simulator.game.gamestate import GameState


class SimulatorPlayer:

    def play_turn(self, gamestate: GameState) -> Action:
        pass

    def get_name(self) -> str:
        pass
