import random
import logging
from typing import List, Dict

from simulator.game.action import Action, PlayAction, ClueAction, DiscardAction
from simulator.game.card import Card
from simulator.game.clue import RankClue
from simulator.game.gamestate import GameState
from simulator.game.rank import Rank
from simulator.game.stack import Stack
from simulator.game.suit import Suit
from simulator.players.simulatorplayer import SimulatorPlayer

logger = logging.getLogger(__name__)


def card_is_trash(card: Card, stacks: Dict[Suit, Stack]):
    stack = stacks[card.suit]
    if stack.last_played is None:
        return False
    return stack.last_played.number_value >= card.number_value


def card_is_discarded(card: Card, discardPile: List[Card]):
    for discardedCard in discardPile:
        if discardedCard.suit == card.suit and discardedCard.rank == card.rank:
            return True
    return False


def get_card_value(card: Card, discardPile: List[Card], stacks: Dict[Suit, Stack]) -> int:

    if card_is_trash(card, stacks):
        return 0

    if card_is_discarded(card, discardPile):
        if card.rank == Rank.ONE:
            return 9
        if card.rank == Rank.TWO:
            return 8
        if card.rank == Rank.THREE:
            return 7
        if card.rank == Rank.FOUR:
            return 6

    if card.rank == Rank.FIVE:
        return 5
    if card.rank == Rank.ONE:
        return 4
    if card.rank == Rank.TWO:
        return 3
    if card.rank == Rank.THREE:
        return 2
    if card.rank == Rank.FOUR:
        return 1

    return 0


class CheatingPlayer(SimulatorPlayer):
    name: str

    def __init__(self):
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

        lowest_value = 999
        lowest_value_slot = -1
        for slot, card in enumerate(my_hand):
            value = get_card_value(card, game.discard_pile, game.stacks)
            if value < lowest_value:
                lowest_value_slot = slot
                lowest_value = value

        logger.debug(self.name + ": Discard slot " + str(lowest_value_slot))
        return DiscardAction(lowest_value_slot)

    def get_name(self) -> str:
        return self.name
