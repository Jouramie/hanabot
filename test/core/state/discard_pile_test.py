from core.state.discard_pile import DiscardPile


def test_new_discard_pile_should_have_no_cards():
    discard_pile = DiscardPile()
    assert len(discard_pile.cards) == 0
