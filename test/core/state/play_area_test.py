import pytest

from core import Variant
from core.state.play_area import PlayArea


@pytest.mark.parametrize("number_suits", [number_suits for number_suits in range(3, 6)])
def test_new_play_area_should_have_empty_stacks(number_suits):
    suits = Variant.get_suits(number_suits)
    play_area = PlayArea(suits)
    assert len(play_area.stacks) == len(suits)
    for suit in suits:
        assert play_area.stacks[suit].last_played is None
