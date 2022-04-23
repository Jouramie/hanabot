from core import Card, Suit, Rank
from core.state.discard_pile import DiscardPile


def test_new_discard_pile_should_have_no_cards():
    discard_pile = DiscardPile()
    assert len(discard_pile.cards) == 0


def test_discarding_should_add_card_to_pile():
    discard_pile = DiscardPile()
    assert len(discard_pile.cards) == 0
    card = Card(Suit.RED, Rank.THREE)
    discard_pile.discard(card)
    assert len(discard_pile.cards) == 1
    assert discard_pile.cards[0] is card


def test_discarding_many_times_should_add_multiple_cards_to_pile():
    discard_pile = DiscardPile()
    cards = [Card(Suit.RED, Rank.THREE),
             Card(Suit.BLUE, Rank.ONE),
             Card(Suit.YELLOW, Rank.FIVE),
             Card(Suit.RED, Rank.ONE)]

    for card in cards:
        discard_pile.discard(card)

    assert len(discard_pile.cards) == len(cards)
    for i in range(0, len(cards)):
        assert discard_pile.cards[i] is cards[i]