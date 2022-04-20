import pytest

from core import Rank


@pytest.mark.parametrize(
    ["rank_to_play", "already_played_rank", "expected_result"],
    [
        (Rank.ONE, None, True),
        (Rank.ONE, Rank.ONE, False),
        (Rank.ONE, Rank.TWO, False),
        (Rank.ONE, Rank.THREE, False),
        (Rank.ONE, Rank.FOUR, False),
        (Rank.ONE, Rank.FIVE, False),
        (Rank.TWO, None, False),
        (Rank.TWO, Rank.ONE, True),
        (Rank.TWO, Rank.TWO, False),
        (Rank.TWO, Rank.THREE, False),
        (Rank.TWO, Rank.FOUR, False),
        (Rank.TWO, Rank.FIVE, False),
        (Rank.THREE, None, False),
        (Rank.THREE, Rank.ONE, False),
        (Rank.THREE, Rank.TWO, True),
        (Rank.THREE, Rank.THREE, False),
        (Rank.THREE, Rank.FOUR, False),
        (Rank.THREE, Rank.FIVE, False),
        (Rank.FOUR, None, False),
        (Rank.FOUR, Rank.ONE, False),
        (Rank.FOUR, Rank.TWO, False),
        (Rank.FOUR, Rank.THREE, True),
        (Rank.FOUR, Rank.FOUR, False),
        (Rank.FOUR, Rank.FIVE, False),
        (Rank.FIVE, None, False),
        (Rank.FIVE, Rank.ONE, False),
        (Rank.FIVE, Rank.TWO, False),
        (Rank.FIVE, Rank.THREE, False),
        (Rank.FIVE, Rank.FOUR, True),
        (Rank.FIVE, Rank.FIVE, False),
    ],
)
def test_given_ranks_combinations_when_is_playable_over_then_is_only_playable_over_one_rank_lower_ranks(rank_to_play, already_played_rank, expected_result):
    assert rank_to_play.is_playable_over(already_played_rank) is expected_result
