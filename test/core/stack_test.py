import pytest

from core import Suit, Rank, Card, Variant
from core.stack import Stack, Stacks

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


def test_given_empty_stack_when_played_cards_then_no_cards_played():
    stack = Stack(A_SUIT)

    played_cards = stack.played_cards

    assert not played_cards


def test_given_stack_at_five_when_played_cards_then_all_suit_played():
    stack = Stack(A_SUIT, Rank.FIVE)

    played_cards = stack.played_cards

    assert played_cards == {Card(A_SUIT, Rank.FIVE), Card(A_SUIT, Rank.FOUR), Card(A_SUIT, Rank.THREE), Card(A_SUIT, Rank.TWO), Card(A_SUIT, Rank.ONE)}


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


def test_given_empty_stacks_when_played_cards_then_no_cards_played():
    stacks = Stacks.create_empty_stacks({A_SUIT})

    played_cards = stacks.played_cards

    assert not played_cards


def test_given_nearly_filled_stacks_when_played_cards_then_find_played_cards():
    stack = Stacks({A_SUIT: Stack(A_SUIT, Rank.FOUR), ANOTHER_SUIT: Stack(ANOTHER_SUIT, Rank.THREE)})

    played_cards = stack.played_cards

    assert played_cards == {
        Card(A_SUIT, Rank.FOUR),
        Card(A_SUIT, Rank.THREE),
        Card(A_SUIT, Rank.TWO),
        Card(A_SUIT, Rank.ONE),
        Card(ANOTHER_SUIT, Rank.THREE),
        Card(ANOTHER_SUIT, Rank.TWO),
        Card(ANOTHER_SUIT, Rank.ONE),
    }


def test_can_play_one_on_zero():
    stack = Stack(Suit.RED)
    can_play = stack.can_play(Card(Suit.RED, Rank.ONE))
    assert can_play


def test_cannot_play_one_on_zero_wrong_suit():
    stack = Stack(Suit.RED)

    with pytest.raises(ValueError):
        stack.can_play(Card(Suit.BLUE, Rank.ONE))


def test_cannot_play_two_on_zero():
    stack = Stack(Suit.RED)
    can_play = stack.can_play(Card(Suit.RED, Rank.TWO))
    assert not can_play


def test_cannot_play_five_on_zero():
    stack = Stack(Suit.RED)
    can_play = stack.can_play(Card(Suit.RED, Rank.FIVE))
    assert not can_play


def test_can_play_two_on_one():
    stack = Stack(Suit.RED, Rank.ONE)
    can_play = stack.can_play(Card(Suit.RED, Rank.TWO))
    assert can_play


def test_cannot_play_three_on_one():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    can_play = stack.can_play(Card(Suit.RED, Rank.THREE))
    assert not can_play


def test_cannot_play_one_on_one():
    stack = Stack(Suit.RED, Rank.ONE)
    can_play = stack.can_play(Card(Suit.RED, Rank.ONE))
    assert not can_play


def test_can_play_three_on_two():
    stack = Stack(Suit.RED, Rank.TWO)
    can_play = stack.can_play(Card(Suit.RED, Rank.THREE))
    assert can_play


def test_cannot_play_four_on_two():
    stack = Stack(Suit.RED, Rank.TWO)
    can_play = stack.can_play(Card(Suit.RED, Rank.FOUR))
    assert not can_play


def test_cannot_play_two_on_two():
    stack = Stack(Suit.RED, Rank.TWO)
    can_play = stack.can_play(Card(Suit.RED, Rank.TWO))
    assert not can_play


def test_stack_score_0():
    stack = Stack(Suit.RED)
    assert stack.stack_score == 0


def test_stack_score_1():
    stack = Stack(Suit.RED, Rank.ONE)
    assert stack.stack_score == 1


def test_stack_score_2():
    stack = Stack(Suit.RED, Rank.TWO)
    assert stack.stack_score == 2


def test_stack_score_3():
    stack = Stack(Suit.RED, Rank.THREE)
    assert stack.stack_score == 3


def test_stack_score_4():
    stack = Stack(Suit.RED, Rank.FOUR)
    assert stack.stack_score == 4


def test_stack_score_5():
    stack = Stack(Suit.RED, Rank.FIVE)
    assert stack.stack_score == 5


def test_stack_score_2_then_mistakes():
    stack = Stack(Suit.RED)
    stack, _ = stack.play(Card(Suit.RED, Rank.ONE))
    stack, _ = stack.play(Card(Suit.RED, Rank.TWO))
    stack, _ = stack.play(Card(Suit.RED, Rank.FOUR))
    stack, _ = stack.play(Card(Suit.RED, Rank.FIVE))
    assert stack.stack_score == 2


def test_stack_score_2_then_mistakes_then_four():
    stack = Stack(Suit.RED)
    stack, _ = stack.play(Card(Suit.RED, Rank.ONE))
    stack, _ = stack.play(Card(Suit.RED, Rank.TWO))
    stack, _ = stack.play(Card(Suit.RED, Rank.ONE))
    stack, _ = stack.play(Card(Suit.RED, Rank.THREE))
    stack, _ = stack.play(Card(Suit.RED, Rank.FOUR))
    assert stack.stack_score == 4


def test_no_cards_no_ranks_played():
    stack = Stack(Suit.RED)
    expected_played_ranks = []
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_one_rank_played():
    stack = Stack(Suit.RED, Rank.ONE)
    expected_played_ranks = [Rank.ONE]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_two_rank_played():
    stack = Stack(Suit.RED, Rank.TWO)
    expected_played_ranks = [Rank.ONE, Rank.TWO]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_three_rank_played():
    stack = Stack(Suit.RED, Rank.THREE)
    expected_played_ranks = [Rank.ONE, Rank.TWO, Rank.THREE]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_four_rank_played():
    stack = Stack(Suit.RED, Rank.FOUR)
    expected_played_ranks = [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_five_rank_played():
    stack = Stack(Suit.RED, Rank.FIVE)
    expected_played_ranks = [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_five_rank_played_two_errors():
    stack = Stack(Suit.RED)
    stack, _ = stack.play(Card(Suit.RED, Rank.ONE))
    stack, _ = stack.play(Card(Suit.RED, Rank.THREE))
    stack, _ = stack.play(Card(Suit.RED, Rank.TWO))
    stack, _ = stack.play(Card(Suit.RED, Rank.THREE))
    expected_played_ranks = [Rank.ONE, Rank.TWO, Rank.THREE]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


@pytest.mark.parametrize("number_suits", [number_suits for number_suits in range(3, 7)])
def test_new_play_area_should_have_empty_stacks(number_suits):
    suits = Variant.get_suits(number_suits)
    play_area = Stacks.create_empty_stacks(suits)
    assert len(play_area) == len(suits)
    assert not play_area.played_cards


def test_play_area_should_say_card_is_playable():
    suits = Variant.get_suits(6)
    play_area = Stacks.create_from_dict(
        {Suit.RED: None, Suit.BLUE: Rank.ONE, Suit.GREEN: Rank.TWO, Suit.YELLOW: Rank.THREE, Suit.PURPLE: Rank.FOUR, Suit.TEAL: Rank.FIVE}, suits
    )

    assert play_area.can_play(Card(Suit.RED, Rank.ONE))
    assert not play_area.can_play(Card(Suit.BLUE, Rank.ONE))
    assert not play_area.can_play(Card(Suit.GREEN, Rank.ONE))
    assert not play_area.can_play(Card(Suit.YELLOW, Rank.ONE))
    assert not play_area.can_play(Card(Suit.PURPLE, Rank.ONE))
    assert not play_area.can_play(Card(Suit.TEAL, Rank.ONE))

    assert not play_area.can_play(Card(Suit.RED, Rank.TWO))
    assert play_area.can_play(Card(Suit.BLUE, Rank.TWO))
    assert not play_area.can_play(Card(Suit.GREEN, Rank.TWO))
    assert not play_area.can_play(Card(Suit.YELLOW, Rank.TWO))
    assert not play_area.can_play(Card(Suit.PURPLE, Rank.TWO))
    assert not play_area.can_play(Card(Suit.TEAL, Rank.TWO))

    assert not play_area.can_play(Card(Suit.RED, Rank.THREE))
    assert not play_area.can_play(Card(Suit.BLUE, Rank.THREE))
    assert play_area.can_play(Card(Suit.GREEN, Rank.THREE))
    assert not play_area.can_play(Card(Suit.YELLOW, Rank.THREE))
    assert not play_area.can_play(Card(Suit.PURPLE, Rank.THREE))
    assert not play_area.can_play(Card(Suit.TEAL, Rank.THREE))

    assert not play_area.can_play(Card(Suit.RED, Rank.FOUR))
    assert not play_area.can_play(Card(Suit.BLUE, Rank.FOUR))
    assert not play_area.can_play(Card(Suit.GREEN, Rank.FOUR))
    assert play_area.can_play(Card(Suit.YELLOW, Rank.FOUR))
    assert not play_area.can_play(Card(Suit.PURPLE, Rank.FOUR))
    assert not play_area.can_play(Card(Suit.TEAL, Rank.FOUR))

    assert not play_area.can_play(Card(Suit.RED, Rank.FIVE))
    assert not play_area.can_play(Card(Suit.BLUE, Rank.FIVE))
    assert not play_area.can_play(Card(Suit.GREEN, Rank.FIVE))
    assert not play_area.can_play(Card(Suit.YELLOW, Rank.FIVE))
    assert play_area.can_play(Card(Suit.PURPLE, Rank.FIVE))
    assert not play_area.can_play(Card(Suit.TEAL, Rank.FIVE))
