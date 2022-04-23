from typing import List

from simulator.game.action import Action
from simulator.game.clue import Clue


class History:
    actions: List[Action]
    clues: List[Clue]

    def __init__(self):
        self.actions = []
        self.clues = []

    def add_clue(self, clue: Clue):
        self.clues.append(clue)

    def add_action(self, action: Action):
        self.actions.append(action)
