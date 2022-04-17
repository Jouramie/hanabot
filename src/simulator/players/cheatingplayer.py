import random
import logging

from simulator.game.action import Action, PlayAction, ClueAction, DiscardAction
from simulator.game.clue import RankClue
from simulator.game.gamestate import GameState
from simulator.players.simulatorplayer import SimulatorPlayer

logger = logging.getLogger(__name__)


class CheatingPlayer(SimulatorPlayer):
    name: str
    log_level: int

    def __init__(self, log_level: int):
        self.log_level = log_level
        self.name = "Cheater #" + str(random.randint(0, 1000))

    def play_turn(self, game: GameState) -> Action:
        myself = game.players[game.player_turn]
        my_hand = myself.hand
        for slot, card in enumerate(my_hand):
            if game.stacks[card.suit].can_play(card):
                logger.debug(self.name + ": Play slot " + str(slot))
                return PlayAction(slot)

        if game.current_clues > 0:
            next_player = game.players[(game.player_turn + 1) % len(game.players)]
            next_player_first_card = next_player.hand[0]
            next_player_first_card_number = next_player_first_card.rank
            logger.debug(self.name + ": Clue " + str(next_player_first_card_number) + " to " + next_player.name)
            return ClueAction(RankClue(next_player_first_card_number, next_player))

        discard_slot = len(my_hand) - 1
        logger.debug(self.name + ": Discard slot " + str(discard_slot))
        return DiscardAction(discard_slot)

    def get_name(self) -> str:
        return self.name
