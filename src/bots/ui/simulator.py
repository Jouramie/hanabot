from bots.domain.decision import DecisionMaking
from simulator.game.action import Action, PlayAction
from simulator.game.gamestate import GameState
from simulator.players.simulatorplayer import SimulatorPlayer


class SimulatorBot(SimulatorPlayer):
    def __init__(self, name: str, decision_making: DecisionMaking):
        super().__init__(name)
        self.decision_making = decision_making

    def play_turn(self, game_state: GameState) -> Action:
        # TODO convert game_state to hanabot game_state
        action = self.decision_making.play_turn(None, None)
        # TODO convert hanabot action to simulator action
        return PlayAction(0)
