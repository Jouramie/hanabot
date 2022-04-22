from dataclasses import dataclass, field
from typing import List

from bots.domain.model.action import Action
from bots.domain.model.player import PlayerHand
from bots.domain.model.stack import Stacks
from core import Card, Rank


@dataclass(frozen=True)
class RelativeGameState:
    stacks: Stacks
    discard: tuple[Card, ...]
    my_hand: PlayerHand
    other_player_hands: tuple[PlayerHand, ...]
    last_performed_action: Action | None
    turn_number: int
    clue_count: int
    bomb_count: int

    def is_first_turn(self):
        return self.last_performed_action is None

    def is_critical(self, card: Card) -> bool:
        # TODO should take into account that card could be unplayable because of the discard
        if card.rank is Rank.FIVE:
            return True

        if card.rank is Rank.ONE:
            return self.discard.count(card) is 2

        return card in self.discard

    def find_not_clued_playable_cards(self):
        pass


@dataclass(frozen=True)
class GameHistory:
    game_states: List[RelativeGameState] = field(default_factory=list)

    def add_game_state(self, game_state: RelativeGameState) -> None:
        self.game_states.append(game_state)
