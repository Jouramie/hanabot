import pytest

from bot.domain.model.stack import Stack, Stacks
from core import Suit, Rank, Card

A_SUIT = Suit.BLUE
ANOTHER_SUIT = Suit.RED


def test_given_empty_stack_when_is_rank_one_playable_then_is_playable():
    stack = Stack(A_SUIT)

    is_one_playable = stack.is_playable(Rank.ONE)

    assert is_one_playable is True


def test_given_empty_stack_when_is_rank_higher_than_one_is_playable_then_is_not_playable():
    stack = Stack(A_SUIT)

    is_playable = stack.is_playable(Rank.FIVE)

    assert is_playable is False


def test_given_started_stack_when_is_next_rank_playable_then_is_playable():
    stack = Stack(A_SUIT, Rank.THREE)

    is_playable = stack.is_playable(Rank.FOUR)

    assert is_playable is True


def test_given_started_stack_when_is_same_rank_playable_then_is_not_playable():
    stack = Stack(A_SUIT, Rank.THREE)

    is_playable = stack.is_playable(Rank.THREE)

    assert is_playable is False


def test_given_started_stack_when_is_lower_rank_playable_then_is_not_playable():
    stack = Stack(A_SUIT, Rank.THREE)

    is_playable = stack.is_playable(Rank.TWO)

    assert is_playable is False


def test_given_empty_stack_when_is_already_played_then_is_not_already_played():
    stack = Stack(A_SUIT)

    is_already_played = stack.is_already_played(Rank.THREE)

    assert is_already_played is False


def test_given_stack_at_five_when_is_already_played_then_is_already_played():
    stack = Stack(A_SUIT, Rank.FIVE)

    is_already_played = stack.is_already_played(Rank.FIVE)

    assert is_already_played is True


def test_given_stack_already_started_when_lower_card_is_already_played_then_is_already_played():
    stack = Stack(A_SUIT, Rank.FOUR)

    is_already_played = stack.is_already_played(Rank.TWO)

    assert is_already_played is True


def test_given_stack_already_started_when_higher_card_is_already_played_then_is_not_already_played():
    stack = Stack(A_SUIT, Rank.ONE)

    is_already_played = stack.is_already_played(Rank.TWO)

    assert is_already_played is False


def test_given_empty_stacks_when_is_one_playable_then_is_playable():
    stacks = Stacks.create_empty_stacks({A_SUIT})

    is_playable = stacks.is_playable(Card(A_SUIT, Rank.ONE))

    assert is_playable is True


def test_given_stacks_when_is_card_from_other_suit_playable_then_no_stack_for_suit():
    stacks = Stacks.create_empty_stacks({A_SUIT})

    with pytest.raises(ValueError):
        stacks.is_playable(Card(ANOTHER_SUIT, Rank.ONE))


def test_given_started_stacks_when_is_lower_rank_card_playable_then_is_playable():
    stacks = Stacks({A_SUIT: Stack(A_SUIT, Rank.TWO)})

    is_playable = stacks.is_playable(Card(A_SUIT, Rank.ONE))

    assert is_playable is False


def test_given_empty_stacks_when_is_card_already_played_then_is_not_already_played():
    stacks = Stacks.create_empty_stacks({A_SUIT})

    is_already_played = stacks.is_already_played(Card(A_SUIT, Rank.TWO))

    assert is_already_played is False


def test_given_started_stacks_when_is_card_already_played_then_is_already_played():
    stacks = Stacks({A_SUIT: Stack(A_SUIT, Rank.TWO)})

    is_already_played = stacks.is_already_played(Card(A_SUIT, Rank.TWO))

    assert is_already_played is True


def test_given_stacks_when_is_card_from_other_suit_already_played_then_no_stack_for_suit():
    stacks = Stacks({A_SUIT: Stack(A_SUIT, Rank.TWO)})

    with pytest.raises(ValueError):
        stacks.is_already_played(Card(ANOTHER_SUIT, Rank.ONE))


def test_given_nearly_filled_stack_when_are_all_playable_or_already_played_then_are_all_playable_or_already_played():
    stacks = Stacks({A_SUIT: Stack(A_SUIT, Rank.FOUR)})

    are_all_playable_or_already_played = stacks.are_all_playable_or_already_played(
        {Card(A_SUIT, Rank.ONE), Card(A_SUIT, Rank.TWO), Card(A_SUIT, Rank.THREE), Card(A_SUIT, Rank.FOUR), Card(A_SUIT, Rank.FIVE)}
    )

    assert are_all_playable_or_already_played is True
