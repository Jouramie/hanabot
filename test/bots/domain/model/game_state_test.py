from __future__ import annotations

from bots.domain.model.action import Action
from bots.domain.model.game_state import RelativeGameState
from bots.domain.model.player import PlayerHand, generate_unknown_hand
from bots.domain.model.stack import Stacks
from core import Card, Suit, Rank

A_SUIT = Suit.TEAL
SOME_SUITS = frozenset({A_SUIT, Suit.RED, Suit.BLUE})
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


class RelativeGameStateBuilder:
    def __init__(self, suits: frozenset[Suit]):
        self.stacks = Stacks.create_empty_stacks(suits)
        self.discard = tuple()
        self.my_hand = PlayerHand("me", generate_unknown_hand(5))
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
