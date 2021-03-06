from __future__ import annotations

from typing import Iterable

from frozendict import frozendict

from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.hand import Hand, HandCard
from core import Card, Suit, Rank, Variant
from core.discard import Discard
from core.stack import Stacks, Stack

ALICE = "Alice"
BOB = "Bob"
CATHY = "Cathy"
DONALD = "Donald"

A_SUIT = Suit.TEAL
ANOTHER_SUIT = Suit.BLUE
SOME_SUITS = frozenset({A_SUIT, Suit.RED, ANOTHER_SUIT})
EMPTY_DISCARD = Discard()


def test_given_empty_discard_when_is_five_critical_then_is_critical():
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard(EMPTY_DISCARD).build()

    is_critical = game_state.is_critical(Card(A_SUIT, Rank.FIVE))

    assert is_critical is True


def test_given_empty_discard_when_is_one_critical_then_is_not_critical():
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard(EMPTY_DISCARD).build()

    is_critical = game_state.is_critical(Card(A_SUIT, Rank.ONE))

    assert is_critical is False


def test_given_discard_with_a_two_when_is_the_other_two_critical_then_is_critical():
    a_two = Card(A_SUIT, Rank.TWO)
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard(Discard(frozendict({a_two: 1}))).build()

    is_critical = game_state.is_critical(a_two)

    assert is_critical is True


def test_given_discard_with_all_four_when_is_five_critical_then_is_not_critical():
    the_five = Card(A_SUIT, Rank.FIVE)
    a_four = Card(A_SUIT, Rank.FOUR)
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard(Discard(frozendict({a_four: 2}))).build()

    is_critical = game_state.is_critical(the_five)

    assert is_critical is False


def test_given_empty_stacks_when_find_playable_cards_then_only_ones_are_playable():
    expected_one_in_bob_hand = HandCard.create_real_card(0, Card(A_SUIT, Rank.ONE))
    expected_one_in_donald_hand = HandCard.create_real_card(0, Card(ANOTHER_SUIT, Rank.ONE))
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks.create_empty_stacks(SOME_SUITS))
        .set_other_player_hands(
            Hand(BOB, (expected_one_in_bob_hand,)),
            Hand(CATHY, (HandCard.create_real_card(0, Card(A_SUIT, Rank.TWO)),)),
            Hand(DONALD, (expected_one_in_donald_hand,)),
        )
        .build()
    )

    playable_cards = list(game_state.find_playable_cards())

    assert playable_cards == [(1, 0, expected_one_in_bob_hand), (3, 0, expected_one_in_donald_hand)]


def test_given_stacks_at_one_when_find_playable_cards_then_only_ones_are_not_playable():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.ONE)}))
        .set_other_player_hands(
            Hand(BOB, ((HandCard.create_real_card(0, Card(A_SUIT, Rank.ONE))),)),
            Hand(CATHY, (HandCard.create_real_card(0, Card(A_SUIT, Rank.THREE)),)),
        )
        .build()
    )

    playable_cards = list(game_state.find_playable_cards())

    assert not playable_cards


def test_given_cards_in_hands_stacks_and_discard_when_visible_cards_then_all_visible_cards_are_found():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.THREE)}))
        .set_other_player_hands(
            Hand(BOB, ((HandCard.create_real_card(0, Card(A_SUIT, Rank.ONE))),)),
            Hand(CATHY, (HandCard.create_real_card(0, Card(A_SUIT, Rank.THREE)),)),
        )
        .set_discard(Discard(frozendict({Card(A_SUIT, Rank.ONE): 1, Card(ANOTHER_SUIT, Rank.FIVE): 1, Card(ANOTHER_SUIT, Rank.ONE): 2})))
        .build()
    )

    visible_cards = game_state.visible_cards

    assert visible_cards == {
        Card(A_SUIT, Rank.ONE): 3,
        Card(A_SUIT, Rank.TWO): 1,
        Card(A_SUIT, Rank.THREE): 2,
        Card(ANOTHER_SUIT, Rank.ONE): 2,
        Card(ANOTHER_SUIT, Rank.FIVE): 1,
    }


def test_given_clued_cards_in_hands_when_clued_cards_then_all_clued_cards_are_found():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.THREE)}))
        .set_other_player_hands(
            Hand(BOB, (HandCard.known_real_card(0, Card(A_SUIT, Rank.ONE)), HandCard.create_real_card(0, Card(ANOTHER_SUIT, Rank.ONE)))),
            Hand(CATHY, (HandCard.create_real_card(0, Card(A_SUIT, Rank.THREE)), HandCard.known_real_card(0, Card(A_SUIT, Rank.FIVE)))),
        )
        .set_discard(Discard(frozendict({Card(A_SUIT, Rank.ONE): 1, Card(ANOTHER_SUIT, Rank.FIVE): 1, Card(ANOTHER_SUIT, Rank.ONE): 1})))
        .build()
    )

    clued_cards = game_state.clued_cards

    assert clued_cards == {Card(A_SUIT, Rank.ONE), Card(A_SUIT, Rank.FIVE)}


def test_given_all_possible_cards_are_visible_except_playable_when_is_possibly_playable_then_is_playable():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.TWO)}))
        .set_other_player_hands(
            Hand(BOB, ((HandCard.create_real_card(0, Card(A_SUIT, Rank.ONE))),)),
            Hand(CATHY, (HandCard.create_real_card(0, Card(A_SUIT, Rank.TWO)),)),
        )
        .set_discard(Discard(frozendict({Card(A_SUIT, Rank.ONE): 1, Card(ANOTHER_SUIT, Rank.FIVE): 1, Card(ANOTHER_SUIT, Rank.ONE): 1})))
        .build()
    )

    is_possibly_playable = game_state.is_possibly_playable(
        HandCard(
            frozenset(
                {
                    Card(A_SUIT, Rank.ONE),
                    Card(A_SUIT, Rank.TWO),
                    Card(A_SUIT, Rank.THREE),
                }
            ),
            True,
            0,
        )
    )

    assert is_possibly_playable is True


def test_given_not_all_possible_cards_are_visible_except_playable_when_is_possibly_playable_then_is_playable():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.TWO)}))
        .set_other_player_hands(
            Hand(BOB, ((HandCard.create_real_card(0, Card(A_SUIT, Rank.ONE))),)),
            Hand(CATHY, (HandCard.create_real_card(0, Card(A_SUIT, Rank.TWO)),)),
        )
        .set_discard(Discard(frozendict({Card(A_SUIT, Rank.ONE): 1, Card(ANOTHER_SUIT, Rank.FIVE): 1, Card(ANOTHER_SUIT, Rank.ONE): 1})))
        .build()
    )

    is_possibly_playable = game_state.is_possibly_playable(
        HandCard(
            frozenset(
                {
                    Card(A_SUIT, Rank.ONE),
                    Card(A_SUIT, Rank.TWO),
                    Card(A_SUIT, Rank.THREE),
                    Card(A_SUIT, Rank.FOUR),
                }
            ),
            True,
            0,
        )
    )

    assert is_possibly_playable is False


class RelativeGameStateBuilder:
    def __init__(self, suits: Iterable[Suit] = Variant.NO_VARIANT):
        self.stacks = Stacks.create_empty_stacks(suits)
        self.discard = Discard()
        self.hands = [Hand.create_unknown_hand(ALICE, 5)]
        self.turn_number = 0
        self.clue_count = 8
        self.strike_count = 0

    @staticmethod
    def from_game_state(game_state: RelativeGameState) -> RelativeGameStateBuilder:
        return (
            RelativeGameStateBuilder()
            .set_stacks(game_state.stacks)
            .set_discard(game_state.discard)
            .set_hands(*game_state.player_hands)
            .set_turn_number(game_state.turn_number)
            .set_clue_count(game_state.clue_count)
            .set_strike_count(game_state.bomb_count)
        )

    def set_stacks(self, stacks: Stacks) -> RelativeGameStateBuilder:
        self.stacks = stacks
        return self

    def set_discard(self, discard: Discard) -> RelativeGameStateBuilder:
        self.discard = discard
        return self

    def set_hands(self, *hands: Hand) -> RelativeGameStateBuilder:
        self.hands = list(hands)
        return self

    def set_my_hand(self, my_hand: Hand) -> RelativeGameStateBuilder:
        self.hands[0] = my_hand
        return self

    def set_other_player_hands(self, *other_player_hands: Hand) -> RelativeGameStateBuilder:
        self.hands = [self.hands[0]] + list(other_player_hands)
        return self

    def set_turn_number(self, turn_number: int) -> RelativeGameStateBuilder:
        self.turn_number = turn_number
        return self

    def set_clue_count(self, clue_count: int) -> RelativeGameStateBuilder:
        self.clue_count = clue_count
        return self

    def set_strike_count(self, strike_count: int) -> RelativeGameStateBuilder:
        self.strike_count = strike_count
        return self

    def build(self) -> RelativeGameState:
        return RelativeGameState(
            stacks=self.stacks,
            discard=self.discard,
            player_hands=tuple(self.hands),
            turn_number=self.turn_number,
            clue_count=self.clue_count,
            bomb_count=self.strike_count,
        )
