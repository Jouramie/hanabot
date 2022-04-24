from core.card import Card, Rank, Suit
from core.state.stack import Stack


def test_can_play_one_on_zero():
    stack = Stack(Suit.RED)
    can_play = stack.can_play(Card(Suit.RED, Rank.ONE))
    assert can_play


def test_cannot_play_one_on_zero_wrong_suit():
    stack = Stack(Suit.RED)
    can_play = stack.can_play(Card(Suit.BLUE, Rank.ONE))
    assert not can_play


def test_cannot_play_two_on_zero():
    stack = Stack(Suit.RED)
    can_play = stack.can_play(Card(Suit.RED, Rank.TWO))
    assert not can_play


def test_cannot_play_five_on_zero():
    stack = Stack(Suit.RED)
    can_play = stack.can_play(Card(Suit.RED, Rank.FIVE))
    assert not can_play


def test_can_play_two_on_one():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    can_play = stack.can_play(Card(Suit.RED, Rank.TWO))
    assert can_play


def test_cannot_play_two_on_one_wrong_suit():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    can_play = stack.can_play(Card(Suit.BLUE, Rank.TWO))
    assert not can_play


def test_cannot_play_three_on_one():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    can_play = stack.can_play(Card(Suit.RED, Rank.THREE))
    assert not can_play


def test_cannot_play_one_on_one():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    can_play = stack.can_play(Card(Suit.RED, Rank.ONE))
    assert not can_play


def test_can_play_three_on_two():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    can_play = stack.can_play(Card(Suit.RED, Rank.THREE))
    assert can_play


def test_cannot_play_three_on_two_wrong_suit():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    can_play = stack.can_play(Card(Suit.BLUE, Rank.THREE))
    assert not can_play


def test_cannot_play_four_on_two():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    can_play = stack.can_play(Card(Suit.RED, Rank.FOUR))
    assert not can_play


def test_cannot_play_two_on_two():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    can_play = stack.can_play(Card(Suit.RED, Rank.TWO))
    assert not can_play


def test_stack_score_0():
    stack = Stack(Suit.RED)
    assert stack.stack_score() == 0


def test_stack_score_1():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    assert stack.stack_score() == 1


def test_stack_score_2():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    assert stack.stack_score() == 2


def test_stack_score_3():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.RED, Rank.THREE))
    assert stack.stack_score() == 3


def test_stack_score_4():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.RED, Rank.THREE))
    stack.play(Card(Suit.RED, Rank.FOUR))
    assert stack.stack_score() == 4


def test_stack_score_5():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.RED, Rank.THREE))
    stack.play(Card(Suit.RED, Rank.FOUR))
    stack.play(Card(Suit.RED, Rank.FIVE))
    assert stack.stack_score() == 5


def test_stack_score_2_then_mistakes():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.BLUE, Rank.THREE))
    stack.play(Card(Suit.RED, Rank.FOUR))
    stack.play(Card(Suit.RED, Rank.FIVE))
    assert stack.stack_score() == 2


def test_stack_score_2_then_mistakes_then_four():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.BLUE, Rank.THREE))
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.THREE))
    stack.play(Card(Suit.RED, Rank.FOUR))
    assert stack.stack_score() == 4


def test_no_cards_no_ranks_played():
    stack = Stack(Suit.RED)
    expected_played_ranks = []
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_one_rank_played():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    expected_played_ranks = [Rank.ONE]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_two_rank_played():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    expected_played_ranks = [Rank.ONE, Rank.TWO]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_three_rank_played():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.RED, Rank.THREE))
    expected_played_ranks = [Rank.ONE, Rank.TWO, Rank.THREE]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_four_rank_played():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.RED, Rank.THREE))
    stack.play(Card(Suit.RED, Rank.FOUR))
    expected_played_ranks = [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_five_rank_played():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.RED, Rank.THREE))
    stack.play(Card(Suit.RED, Rank.FOUR))
    stack.play(Card(Suit.RED, Rank.FIVE))
    expected_played_ranks = [Rank.ONE, Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1


def test_five_rank_played_two_errors():
    stack = Stack(Suit.RED)
    stack.play(Card(Suit.RED, Rank.ONE))
    stack.play(Card(Suit.BLUE, Rank.TWO))
    stack.play(Card(Suit.RED, Rank.THREE))
    stack.play(Card(Suit.RED, Rank.TWO))
    stack.play(Card(Suit.RED, Rank.THREE))
    expected_played_ranks = [Rank.ONE, Rank.TWO, Rank.THREE]
    played_ranks = stack.get_ranks_already_played()
    assert len(played_ranks) == len(expected_played_ranks)
    for rank in expected_played_ranks:
        assert played_ranks.count(rank) == 1
