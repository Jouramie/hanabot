from typing import List

from simulator.game.action import Action
from simulator.game.clue import Clue


class History:
    actions: List[Action]
    clues: List[Clue]

    def __init__(self):
        self.actions = []
        self.clues = []
