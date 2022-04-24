from __future__ import annotations

from typing import Iterable

from bots.domain.model.action import Action
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerHand, create_unknown_hand, create_unknown_real_card, PlayerCard, create_known_real_card
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

    assert playable_cards == [(1, 0, expected_one_in_bob_hand), (3, 0, expected_one_in_donald_hand)]


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


def test_given_cards_in_hands_stacks_and_discard_when_visible_cards_then_all_visible_cards_are_found():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.THREE)}))
        .set_other_player_hands(
            (
                PlayerHand(BOB, ((create_unknown_real_card(Card(A_SUIT, Rank.ONE))),)),
                PlayerHand(CATHY, (create_unknown_real_card(Card(A_SUIT, Rank.THREE)),)),
            )
        )
        .set_discard((Card(A_SUIT, Rank.ONE), Card(ANOTHER_SUIT, Rank.FIVE), Card(ANOTHER_SUIT, Rank.ONE)))
        .build()
    )

    visible_cards = game_state.visible_cards

    assert visible_cards == {
        Card(A_SUIT, Rank.ONE): 3,
        Card(A_SUIT, Rank.TWO): 1,
        Card(A_SUIT, Rank.THREE): 2,
        Card(ANOTHER_SUIT, Rank.ONE): 1,
        Card(ANOTHER_SUIT, Rank.FIVE): 1,
    }


def test_given_clued_cards_in_hands_when_clued_cards_then_all_clued_cards_are_found():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.THREE)}))
        .set_other_player_hands(
            (
                PlayerHand(BOB, (create_known_real_card(Card(A_SUIT, Rank.ONE)), create_unknown_real_card(Card(ANOTHER_SUIT, Rank.ONE)))),
                PlayerHand(CATHY, (create_unknown_real_card(Card(A_SUIT, Rank.THREE)), create_known_real_card(Card(A_SUIT, Rank.FIVE)))),
            )
        )
        .set_discard((Card(A_SUIT, Rank.ONE), Card(ANOTHER_SUIT, Rank.FIVE), Card(ANOTHER_SUIT, Rank.ONE)))
        .build()
    )

    clued_cards = game_state.clued_cards

    assert clued_cards == {Card(A_SUIT, Rank.ONE), Card(A_SUIT, Rank.FIVE)}


def test_given_all_possible_cards_are_visible_except_playable_when_is_possibly_playable_then_is_playable():
    game_state = (
        RelativeGameStateBuilder(SOME_SUITS)
        .set_stacks(Stacks({A_SUIT: Stack(A_SUIT, Rank.TWO)}))
        .set_other_player_hands(
            (
                PlayerHand(BOB, ((create_unknown_real_card(Card(A_SUIT, Rank.ONE))),)),
                PlayerHand(CATHY, (create_unknown_real_card(Card(A_SUIT, Rank.TWO)),)),
            )
        )
        .set_discard((Card(A_SUIT, Rank.ONE), Card(ANOTHER_SUIT, Rank.FIVE), Card(ANOTHER_SUIT, Rank.ONE)))
        .build()
    )

    is_possibly_playable = game_state.is_possibly_playable(
        PlayerCard(
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
            (
                PlayerHand(BOB, ((create_unknown_real_card(Card(A_SUIT, Rank.ONE))),)),
                PlayerHand(CATHY, (create_unknown_real_card(Card(A_SUIT, Rank.TWO)),)),
            )
        )
        .set_discard((Card(A_SUIT, Rank.ONE), Card(ANOTHER_SUIT, Rank.FIVE), Card(ANOTHER_SUIT, Rank.ONE)))
        .build()
    )

    is_possibly_playable = game_state.is_possibly_playable(
        PlayerCard(
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
    def __init__(self, suits: Iterable[Suit]):
        self.stacks = Stacks.create_empty_stacks(suits)
        self.discard = tuple()
        self.hands = [create_unknown_hand(ALICE, 5)]
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
        self.hands[0] = my_hand
        return self

    def set_other_player_hands(self, other_player_hands: tuple[PlayerHand, ...]) -> RelativeGameStateBuilder:
        self.hands = [self.hands[0]] + list(other_player_hands)
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
            player_hands=tuple(self.hands),
            last_performed_action=self.last_performed_action,
            turn_number=self.turn_number,
            clue_count=self.clue_count,
            bomb_count=self.strike_count,
        )
