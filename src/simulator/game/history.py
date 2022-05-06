from core.state.gamestate import GameState
from simulator.game.action import Action
from simulator.game.clue import Clue


class History:
    actions: list[Action]
    clues: list[Clue]
    gamestates: list[GameState]

    def __init__(self):
        self.actions = []
        self.clues = []
        self.gamestates = []

    def add_clue(self, clue: Clue):
        self.clues.append(clue)

    def add_action(self, action: Action):
        self.actions.append(action)

    def add_state(self, gamestate: GameState):
        self.gamestates.append(gamestate)

    def get_state_at_turn(self, turn: int) -> GameState:
        return self.gamestates[turn]
