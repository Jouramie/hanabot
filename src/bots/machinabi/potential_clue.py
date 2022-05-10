from bots.domain.decision import SuitClueDecision, RankClueDecision, ClueDecision
from bots.machinabi.analysed_clue import ClueType


class PotentialClue:
    clue: ClueDecision

    def __init__(self, clue: ClueDecision):
        self.clue = clue

    @property
    def value(self) -> float:
        return 0
