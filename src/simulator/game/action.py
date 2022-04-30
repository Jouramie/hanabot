from core.card import Card, Suit, Rank
from simulator.game.player import Player


class Action:
    turn: int
    actor: Player

    def act_on_state(self, gamestate):
        pass


class ColorClueAction(Action):
    color: Suit
    target_player: Player

    def __init__(self, color: Suit, player: Player):
        self.color = color
        self.target_player = player

    def act_on_state(self, gamestate):
        gamestate.play_turn_color_clue(self)

    def __str__(self):
        return f"{self.actor.name} clued {self.target_player.name} {self.color.name}."


class RankClueAction(Action):
    rank: Rank
    target_player: Player

    def __init__(self, rank: Rank, player: Player):
        self.rank = rank
        self.target_player = player

    def act_on_state(self, gamestate):
        gamestate.play_turn_rank_clue(self)

    def __str__(self):
        return f"{self.actor.name} clued {self.target_player.name} {self.rank.name}."


class PlayAction(Action):
    playedCard: Card
    cardSlot: int
    drawId: int
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
    drawId: int

    def __init__(self, slot: int):
        self.cardSlot = slot

    def act_on_state(self, gamestate):
        gamestate.play_turn_discard(self)

    def __str__(self):
        return f"{self.actor.name} discarded {repr(self.discardedCard)} from slot {self.cardSlot + 1}."
