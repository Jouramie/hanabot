from bot.domain.hanabot import Hanabot
from simulator.game.action import Action
from simulator.game.gamestate import GameState
from simulator.players.simulatorplayer import SimulatorPlayer


class SimulatorPlayerAdapter(SimulatorPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.hanabot = Hanabot(name, set())

    def play_turn(self, gamestate: GameState) -> Action:
        pass
