from dataclasses import dataclass, field
from functools import cached_property
from typing import List, Iterable, Dict

from bots.domain.model.action import Action
from bots.domain.model.player import PlayerHand, PlayerCard, RelativePlayerNumber, Slot
from bots.domain.model.stack import Stacks
from core import Card, Rank


@dataclass(frozen=True)
class RelativeGameState:
    stacks: Stacks
    discard: tuple[Card, ...]
    player_hands: tuple[PlayerHand, ...]
    last_performed_action: Action | None
    turn_number: int
    clue_count: int
    bomb_count: int

    _visible_cards = None

    def is_first_turn(self):
        return self.last_performed_action is None

    def is_critical(self, card: Card) -> bool:
        # TODO should take into account that card could be unplayable because of the discard
        if card.rank is Rank.FIVE:
            return True

        if card.rank is Rank.ONE:
            return self.discard.count(card) == 2

        return card in self.discard

    def find_playable_cards(self) -> Iterable[tuple[RelativePlayerNumber, Slot, PlayerCard]]:
        for relative_player_id, hand in enumerate(self.other_player_hands, 1):
            for slot, card in enumerate(hand.cards):
                if self.stacks.is_playable(card.real_card):
                    yield relative_player_id, slot, card

    @property
    def my_hand(self) -> PlayerHand:
        return self.player_hands[0]

    @property
    def other_player_hands(self) -> tuple[PlayerHand]:
        return self.player_hands[1:]

    def can_give_clue(self):
        return self.clue_count > 0

    def can_discard(self):
        return self.clue_count < 8

    def is_possibly_playable(self, card: PlayerCard):
        filtered_possible_cards = set()
        visible_cards = self.visible_cards
        for possible_card in card.interpreted_cards:
            if visible_cards.get(possible_card, 0) < possible_card.number_of_copies:
                filtered_possible_cards.add(possible_card)

        return self.stacks.are_all_playable_or_already_played(filtered_possible_cards)

    @cached_property
    def visible_cards(self) -> Dict[Card, int]:
        visible_cards = {}
        for card in self.stacks.played_cards:
            visible_cards[card] = visible_cards.get(card, 0) + 1

        for card in self.discard:
            visible_cards[card] = visible_cards.get(card, 0) + 1

        for hand in self.other_player_hands:
            for card in hand.cards:
                visible_cards[card.real_card] = visible_cards.get(card.real_card, 0) + 1

        return visible_cards

    def is_playable(self, card: Card) -> bool:
        return self.stacks.is_playable(card)


@dataclass(frozen=True)
class GameHistory:
    game_states: List[RelativeGameState] = field(default_factory=list)

    def add_game_state(self, game_state: RelativeGameState) -> None:
        self.game_states.append(game_state)

    @property
    def action_history(self) -> list[Action]:
        return [game_state.last_performed_action for game_state in self.game_states]
