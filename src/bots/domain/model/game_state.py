from dataclasses import dataclass, field
from functools import cached_property, reduce
from typing import List, Iterable

from bots.domain.model.action import Action
from bots.domain.model.hand import Hand, HandCard, Slot, DrawId
from bots.domain.model.stack import Stacks
from core import Card, all_possible_cards

RelativePlayerNumber = int


@dataclass(frozen=True)
class RelativeGameState:
    stacks: Stacks
    discard: tuple[Card, ...]
    player_hands: tuple[Hand, ...]
    last_performed_action: Action | None
    turn_number: int
    clue_count: int
    bomb_count: int

    _visible_cards = None

    def is_first_turn(self):
        return self.last_performed_action is None

    def is_critical(self, card: Card) -> bool:
        if self.is_trash(card):
            return False

        if card.number_of_copies == 1:
            return True

        return card.number_of_copies == 2 and card in self.discard

    def is_trash(self, card: Card) -> bool:
        is_already_played = self.is_already_played(card)
        if is_already_played:
            return True

        previous_card = card.previous_card
        while previous_card is not None:
            count = reduce(lambda x, y: x + y, [1 for discarded in self.discard if discarded == previous_card], 0)
            if count == previous_card.number_of_copies:
                return True
            previous_card = previous_card.previous_card
        return False

    def is_possibly_playable(self, card: HandCard) -> bool:
        filtered_possible_cards = set()
        visible_cards = self.visible_cards
        for possible_card in card.notes_on_cards:
            if visible_cards.get(possible_card, 0) < possible_card.number_of_copies:
                filtered_possible_cards.add(possible_card)

        return self.stacks.are_all_playable_or_already_played(filtered_possible_cards)

    def is_playable(self, card: Card) -> bool:
        return self.stacks.is_playable(card)

    def is_playable_over_clued_playable(self, card: Card) -> bool:
        for clued_playable_card in self.clued_playable_cards:
            if card.is_playable_over(clued_playable_card):
                return True

    def is_already_played(self, card: Card) -> bool:
        return self.stacks.is_already_played(card)

    def is_already_clued(self, card: Card) -> bool:
        return card in self.clued_cards

    def find_not_clued_playable_cards(self) -> Iterable[tuple[RelativePlayerNumber, Slot, HandCard]]:
        for relative_player_id, slot, card in self.find_playable_cards():
            if card.real_card not in self.clued_cards:
                yield relative_player_id, slot, card

    def find_not_known_playable_cards(self) -> Iterable[tuple[RelativePlayerNumber, Slot, HandCard]]:
        for relative_player_id, slot, card in self.find_playable_cards():
            if not card.is_fully_known:
                yield relative_player_id, slot, card

    def find_playable_cards(self) -> Iterable[tuple[RelativePlayerNumber, Slot, HandCard]]:
        for relative_player_id, hand in enumerate(self.other_player_hands, 1):
            for slot, card in enumerate(hand.cards):
                if self.stacks.is_playable(card.real_card):
                    yield relative_player_id, slot, card

    def find_not_clued_critical(self) -> Iterable[Card]:
        for card in self.my_hand.cards:
            if self.is_critical(card.real_card) and not card.is_clued:
                yield card.real_card

    def find_missing_cards_to_play(self, card: Card) -> list[Card]:
        return [
            missing_card for missing_card in all_possible_cards(suits=card.suit) if missing_card.rank < card.rank and not self.is_already_played(missing_card)
        ]

    def find_hand_card(self, searched_card: Card) -> list[tuple[RelativePlayerNumber, Slot, HandCard]]:
        return [
            (relative_player_id, slot, card)
            for relative_player_id, hand in enumerate(self.other_player_hands, 1)
            for slot, card in enumerate(hand.cards)
            if card.real_card == searched_card
        ]

    def find_card_by_draw_id(self, draw_id: DrawId) -> HandCard | None:
        for hand in self.player_hands:
            for card in hand.cards:
                if card.draw_id == draw_id:
                    return card

    @property
    def my_hand(self) -> Hand:
        return self.player_hands[0]

    @property
    def other_player_hands(self) -> tuple[Hand]:
        return self.player_hands[1:]

    def find_player_hand(self, player_name: str) -> Hand:
        for hand in self.player_hands:
            if hand.owner_name == player_name:
                return hand

    def can_give_clue(self):
        return self.clue_count > 0

    def can_discard(self):
        return self.clue_count < 8

    @cached_property
    def visible_cards(self) -> dict[Card, int]:
        visible_cards = {}
        for card in self.stacks.played_cards:
            visible_cards[card] = visible_cards.get(card, 0) + 1

        for card in self.discard:
            visible_cards[card] = visible_cards.get(card, 0) + 1

        for hand in self.other_player_hands:
            for card in hand.cards:
                visible_cards[card.real_card] = visible_cards.get(card.real_card, 0) + 1

        return visible_cards

    @property
    def clued_cards(self) -> set[Card]:
        clued_cards = set()
        for hand in self.other_player_hands:
            for card in hand.cards:
                if card.is_clued:
                    clued_cards.add(card.real_card)

        return clued_cards

    @property
    def clued_playable_cards(self) -> set[Card]:
        clued_playable_cards = set()
        for card in self.clued_cards:
            if self.is_playable(card):
                clued_playable_cards.add(card)

        return clued_playable_cards


@dataclass(frozen=True)
class GameHistory:
    game_states: List[RelativeGameState] = field(default_factory=list)

    def add_game_state(self, game_state: RelativeGameState) -> None:
        self.game_states.append(game_state)

    @property
    def action_history(self) -> list[Action]:
        return [game_state.last_performed_action for game_state in self.game_states]
