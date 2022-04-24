import pytest

from core import Variant, Card, Suit, Rank
from core.state.play_area import PlayArea


@pytest.mark.parametrize("number_suits", [number_suits for number_suits in range(3, 6)])
def test_new_play_area_should_have_empty_stacks(number_suits):
    suits = Variant.get_suits(number_suits)
    play_area = PlayArea(suits)
    assert len(play_area.stacks) == len(suits)
    for suit in suits:
        assert play_area.stacks[suit].last_played is None


def test_play_area_should_say_card_is_playable():
    suits = Variant.get_suits(6)
    play_area = PlayArea(suits)
    play_area.stacks[Suit.RED].last_played = None
    play_area.stacks[Suit.BLUE].last_played = Rank.ONE
    play_area.stacks[Suit.GREEN].last_played = Rank.TWO
    play_area.stacks[Suit.YELLOW].last_played = Rank.THREE
    play_area.stacks[Suit.PURPLE].last_played = Rank.FOUR
    play_area.stacks[Suit.TEAL].last_played = Rank.FIVE

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