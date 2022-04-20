import pytest

from bot.domain.model.stack import Stack
from core import Suit, Rank


@pytest.mark.skip
def test_given_empty_stack_when_is_rank_one_playable_then_is_playable():
    stack = Stack(Suit.RED)

    is_one_playable = stack.is_playable(Rank.ONE)

    assert is_one_playable is True


@pytest.mark.skip
@pytest.mark.parametrize("rank", [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE])
def test_given_empty_stack_when_is_rank_higher_than_one_is_playable_then_is_not_playable(rank: Rank):
    stack = Stack(Suit.RED)

    is_one_playable = stack.is_playable(rank)

    assert is_one_playable is False
