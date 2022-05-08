from core import Card, Suit, Rank
from core.discard import Discard


def test_new_discard_pile_should_have_no_cards():
    discard_pile = Discard()
    assert len(discard_pile) == 0


def test_discarding_should_add_card_to_pile():
    discard_pile = Discard()
    card = Card(Suit.RED, Rank.THREE)
    discard_pile = discard_pile.discard(card)
    assert len(discard_pile) == 1
    assert discard_pile.count(card) == 1


def test_discarding_many_times_should_add_multiple_cards_to_pile():
    discard_pile = Discard()
    cards = [Card(Suit.RED, Rank.THREE), Card(Suit.BLUE, Rank.ONE), Card(Suit.YELLOW, Rank.FIVE), Card(Suit.BLUE, Rank.ONE)]

    for card in cards:
        discard_pile = discard_pile.discard(card)

    assert len(discard_pile) == len(cards)
