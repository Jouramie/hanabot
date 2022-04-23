from __future__ import annotations

from bots.domain.model.action import Action
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerHand, create_unknown_hand, create_unknown_real_card
from bots.domain.model.stack import Stacks, Stack
from core import Card, Suit, Rank

ALICE = "Alice"
BOB = "Bob"
CATHY = "Cathy"
DONALD = "Donald"

A_SUIT = Suit.TEAL
ANOTHER_SUIT = Suit.BLUE
SOME_SUITS = frozenset({A_SUIT, Suit.RED, ANOTHER_SUIT})
EMPTY_DISCARD = tuple()


def test_given_empty_discard_when_is_five_critical_then_is_critical():
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard(EMPTY_DISCARD).build()

    is_five_critical = game_state.is_critical(Card(A_SUIT, Rank.FIVE))

    assert is_five_critical is True


def test_given_empty_discard_when_is_one_critical_then_is_not_critical():
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard(EMPTY_DISCARD).build()

    is_five_critical = game_state.is_critical(Card(A_SUIT, Rank.ONE))

    assert is_five_critical is False


def test_given_discard_with_a_two_when_is_the_other_two_critical_then_is_critical():
    a_two = Card(A_SUIT, Rank.TWO)
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard((a_two,)).build()

    is_five_critical = game_state.is_critical(a_two)

    assert is_five_critical is True


def test_given_discard_with_a_one_when_is_the_last_one_critical_then_is_not_critical():
    a_one = Card(A_SUIT, Rank.ONE)
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard((a_one,)).build()

    is_five_critical = game_state.is_critical(a_one)

    assert is_five_critical is False


def test_given_discard_with_two_ones_when_is_the_last_one_critical_then_is_critical():
    a_one = Card(A_SUIT, Rank.ONE)
    game_state = RelativeGameStateBuilder(SOME_SUITS).set_discard((a_one, a_one)).build()

    is_five_critical = game_state.is_critical(a_one)

    assert is_five_critical is True


def test_given_empty_stacks_when_find_playable_cards_then_only_ones_are_playable():
    expected_one_in_bob_hand = create_unknown_real_card(Card(A_SUIT, Rank.ONE))
    expected_one_in_donald_hand = create_unknown_real_card(Card(ANOTHER_SUIT, Rank.ONE))
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks.create_empty_stacks(SOME_SUITS))
        .set_other_player_hands(
            (
                PlayerHand(BOB, (expected_one_in_bob_hand,)),
                PlayerHand(CATHY, (create_unknown_real_card(Card(A_SUIT, Rank.TWO)),)),
                PlayerHand(DONALD, (expected_one_in_donald_hand,)),
            )
        )
        .build()
    )

    playable_cards = list(game_state.find_playable_cards())

    assert playable_cards == [(BOB, 0, expected_one_in_bob_hand), (DONALD, 0, expected_one_in_donald_hand)]


def test_given_stacks_at_one_when_find_playable_cards_then_only_ones_are_not_playable():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.ONE)}))
        .set_other_player_hands(
            (
                PlayerHand(BOB, ((create_unknown_real_card(Card(A_SUIT, Rank.ONE))),)),
                PlayerHand(CATHY, (create_unknown_real_card(Card(A_SUIT, Rank.THREE)),)),
            )
        )
        .build()
    )

    playable_cards = list(game_state.find_playable_cards())

    assert not playable_cards


class RelativeGameStateBuilder:
    def __init__(self, suits: frozenset[Suit]):
        self.stacks = Stacks.create_empty_stacks(suits)
        self.discard = tuple()
        self.my_hand = create_unknown_hand(ALICE, 5)
        self.other_player_hands = tuple()
        self.last_performed_action = None
        self.turn_number = 0
        self.clue_count = 8
        self.strike_count = 0

    def set_stacks(self, stacks: Stacks) -> RelativeGameStateBuilder:
        self.stacks = stacks
        return self

    def set_discard(self, discard: tuple[Card, ...]) -> RelativeGameStateBuilder:
        self.discard = discard
        return self

    def set_my_hand(self, my_hand: PlayerHand) -> RelativeGameStateBuilder:
        self.my_hand = my_hand
        return self

    def set_other_player_hands(self, other_player_hands: tuple[PlayerHand, ...]) -> RelativeGameStateBuilder:
        self.other_player_hands = other_player_hands
        return self

    def set_last_performed_action(self, last_performed_action: Action) -> RelativeGameStateBuilder:
        self.last_performed_action = last_performed_action
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
            my_hand=self.my_hand,
            other_player_hands=self.other_player_hands,
            last_performed_action=self.last_performed_action,
            turn_number=self.turn_number,
            clue_count=self.clue_count,
            bomb_count=self.strike_count,
        )
