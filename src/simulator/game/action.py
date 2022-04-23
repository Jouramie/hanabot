from core.card import Card
from simulator.game.clue import Clue, ColorClue
from simulator.game.player import Player


class Action:
    turn: int
    actor: Player

    def act_on_state(self, gamestate):
        pass


class ClueAction(Action):
    clue: Clue

    def __init__(self, clue: Clue):
        self.clue = clue

    def act_on_state(self, gamestate):
        gamestate.play_turn_clue(self)

    def __str__(self):
        if type(self.clue) is ColorClue:
            return f"{self.clue.giver.name} clued {self.clue.receiver.name} {self.clue.suit.name}."
        else:
            return f"{self.clue.giver.name} clued {self.clue.receiver.name} {self.clue.rank.name}."


class PlayAction(Action):
    playedCard: Card
    cardSlot: int
    success: bool

    def __init__(self, slot: int):
        self.cardSlot = slot

    def act_on_state(self, gamestate):
        gamestate.play_turn_play(self)

    def __str__(self):
        return f"{self.actor.name} played {repr(self.playedCard)} from slot {self.cardSlot + 1}."


class DiscardAction(Action):
    discardedCard: Card
    cardSlot: int

    def __init__(self, slot: int):
        self.cardSlot = slot

    def act_on_state(self, gamestate):
        gamestate.play_turn_discard(self)

    def __str__(self):
        return f"{self.actor.name} discarded {repr(self.discardedCard)} from slot {self.cardSlot + 1}."
