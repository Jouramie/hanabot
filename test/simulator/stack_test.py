from simulator.game.card import Card, Suit, Rank
from simulator.game.stack import Stack


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