from bot.domain.hanabot import Hanabot
from simulator.game.action import Action, PlayAction
from simulator.game.gamestate import GameState
from simulator.players.simulatorplayer import SimulatorPlayer


class SimulatorPlayerAdapter(SimulatorPlayer):
    def __init__(self, name):
        super().__init__(name)
        self.hanabot = Hanabot(name, set())

    def play_turn(self, gamestate: GameState) -> Action:
        # TODO convert gamestate to hanabot gamestate
        action = self.hanabot.play_turn(None, None)
        # TODO convert hanabot action to simulator action
        return PlayAction(0)
