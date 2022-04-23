from dataclasses import dataclass, field
from typing import List, Iterable

from bots.domain.model.action import Action
from bots.domain.model.player import PlayerHand, PlayerCard
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

    def find_playable_cards(self) -> Iterable[tuple[int, int, PlayerCard]]:
        for hand in self.other_player_hands:
            for i, card in enumerate(hand.cards):
                if self.stacks.is_playable(card.real_card):
                    yield hand.owner, i, card


@dataclass(frozen=True)
class GameHistory:
    game_states: List[RelativeGameState] = field(default_factory=list)

    def add_game_state(self, game_state: RelativeGameState) -> None:
        self.game_states.append(game_state)
