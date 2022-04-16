import random

from simulator.game.action import Action, PlayAction, ClueAction, DiscardAction
from simulator.game.clue import RankClue
from simulator.game.gamestate import GameState
from simulator.players.simulatorplayer import SimulatorPlayer


class CheatingPlayer(SimulatorPlayer):
    name: str

    def __init__(self):
        self.name = "Cheater #" + str(random.randint(0, 1000))

    def play_turn(self, game: GameState) -> Action:
        myself = game.players[game.playerTurn]
        my_hand = myself.hand
        for slot, card in my_hand:
            if game.stacks[card.suit].can_play(card):
                return PlayAction(slot)

        if game.currentClues > 0:
            next_player = game.players[(game.playerTurn + 1) % len(game.players)]
            next_player_first_card = next_player.hand[0]
            next_player_first_card_number = next_player_first_card.rank
            return ClueAction(RankClue(next_player_first_card_number, next_player))

        return DiscardAction(len(my_hand) - 1)

    def get_name(self) -> str:
        return self.name
