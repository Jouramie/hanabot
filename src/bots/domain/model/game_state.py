from __future__ import annotations

from dataclasses import dataclass, field
from functools import cached_property
from typing import List, Iterable

from bots.domain.model.action import Action
from bots.domain.model.hand import Hand, HandCard, Slot, DrawId
from core import Card, all_possible_cards, Rank
from core.discard import Discard
from core.stack import Stacks

RelativePlayerNumber = int


@dataclass(frozen=True)
class RelativeGameState:
    stacks: Stacks
    discard: Discard
    player_hands: tuple[Hand, ...]
    turn_number: int
    clue_count: int
    bomb_count: int

    def is_critical(self, card: Card) -> bool:
        if self.is_trash(card):
            return False

        if card.number_of_copies == 1:
            return True

        return card.number_of_copies == 2 and card in self.discard

    def is_trash(self, card: Card) -> bool:
        if self.is_already_played(card):
            return True

        previous_card = card.previous_card
        while previous_card is not None:
            count = self.discard.count(previous_card)
            if count == previous_card.number_of_copies:
                return True
            previous_card = previous_card.previous_card
        return False

    def is_already_played(self, card: Card) -> bool:
        return self.stacks.is_already_played(card)

    def is_eventually_playable(self, card: Card) -> bool:
        return not self.is_trash(card)

    def are_all_eventually_playable(self, cards: Iterable[Card]) -> bool:
        return all(self.is_eventually_playable(card) for card in cards)

    def is_already_clued(self, card: Card) -> bool:
        return card in self.clued_cards

    def are_any_already_clued(self, cards: Iterable[Card]) -> bool:
        return any(self.is_already_clued(card) for card in cards)

    def is_possibly_playable(self, card: HandCard) -> bool:
        filtered_possible_cards = set()
        visible_cards = self.visible_cards
        for possible_card in card.notes_on_cards:
            if visible_cards.get(possible_card, 0) < possible_card.number_of_copies:
                filtered_possible_cards.add(possible_card)

        return self.stacks.are_all_playable_or_already_played(filtered_possible_cards)

    def is_playable(self, card: Card) -> bool:
        return self.stacks.is_playable(card)

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
                if self.is_playable(card.real_card):
                    yield relative_player_id, slot, card

    def find_not_clued_critical_cards(self) -> Iterable[tuple[RelativePlayerNumber, Slot, HandCard]]:
        for relative_player_id, hand in enumerate(self.other_player_hands, 1):
            for slot, card in enumerate(hand.cards):
                if self.is_critical(card.real_card) and not card.is_clued:
                    yield relative_player_id, slot, card

    def find_missing_cards_to_play(self, card: Card) -> list[Card]:
        return [
            missing_card for missing_card in all_possible_cards(suits=card.suit) if missing_card.rank < card.rank and not self.is_already_played(missing_card)
        ]

    def find_hand_card(self, searched_card: Card) -> list[tuple[RelativePlayerNumber, Slot, HandCard]]:
        return [
            (relative_player_id, slot, card)
            for relative_player_id, hand in enumerate(self.player_hands)
            for slot, card in enumerate(hand.cards)
            if card.real_card == searched_card or card.fully_known_card == searched_card
        ]

    def find_card_by_draw_id(self, draw_id: DrawId) -> HandCard | None:
        for hand in self.player_hands:
            for card in hand.cards:
                if card.draw_id == draw_id:
                    return card

    def find_clued_cards_leading_to(self, card: Card) -> list[tuple[RelativePlayerNumber, Slot, HandCard]] | None:
        last_card_played = self.stacks.last_card_played_on_stack(card.suit)
        if last_card_played is None:
            start = Card(card.suit, Rank.ONE)
        else:
            start = last_card_played.next_card

        cards_leading_to = []
        for searched_card in Card.range(start, card):
            found_cards = self.find_clued(searched_card)
            if not found_cards:
                return
            cards_leading_to.extend(found_cards)
        return cards_leading_to

    def find_clued(self, searched_card: Card) -> list[tuple[RelativePlayerNumber, Slot, HandCard]]:
        return [(relative_player_id, slot, card) for relative_player_id, slot, card in self.find_hand_card(searched_card) if card.is_clued]

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
            visible_cards[card] = visible_cards.get(card, 0) + self.discard.count(card)

        for hand in self.player_hands:
            for card in hand.cards:
                known_card = card.real_or_fully_known_card
                if known_card is not None:
                    visible_cards[known_card] = visible_cards.get(known_card, 0) + 1

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
class Turn:
    previous_game_state: RelativeGameState
    action: Action
    resulting_game_state: RelativeGameState


@dataclass(frozen=True)
class GameHistory:
    turns: List[Turn] = field(default_factory=list)

    def add_game_state(self, turn: Turn) -> None:
        self.turns.append(turn)

    def __getitem__(self, item):
        return self.turns[item]

    @property
    def latest_turn_number(self) -> int:
        return len(self.turns) - 1
