import random

from simulator.game.action import Action
from simulator.game.gamestate import GameState
from simulator.players.simulatorplayer import SimulatorPlayer


class Machinabi(SimulatorPlayer):
    def __init__(self):
        super().__init__("Machinabi #" + str(random.randint(0, 1000)))

    def play_turn(self, game: GameState) -> Action:
        pass