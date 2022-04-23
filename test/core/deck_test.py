from core import Card, Rank, Suit
from core.deck import Deck


def test_when_generate_default_deck_then_deck_has_50_cards():
    deck = Deck.generate()

    assert len(deck) == 50


def test_given_default_deck_when_draw_then_deck_has_49_cards():
    deck = Deck.generate()

    deck.draw()

    assert len(deck) == 49


def test_given_starting_with_a_card_when_draw_then_drawn_card_it_the_card():
    the_card = Card(Suit.PURPLE, Rank.TWO)
    deck = Deck.starting_with(the_card)

    drawn_card = deck.draw()

    assert drawn_card == the_card


def test_given_starting_with_three_cards_when_pick_third_card_then_drawn_card_it_the_third_card():
    third_card = Card(Suit.RED, Rank.FIVE)
    deck = Deck.starting_with([Card(Suit.RED, Rank.FOUR), Card(Suit.YELLOW, Rank.ONE), third_card])

    drawn_card = deck[2]

    assert drawn_card == third_card


def test_when_generate_default_deck_then_deck_is_not_empty():
    deck = Deck.generate()

    assert not deck.is_empty()


def test_given_default_deck_when_draw_50_times_then_deck_is_empty():
    deck = Deck.generate()

    for _ in range(50):
        deck.draw()

    assert deck.is_empty()
    assert deck.is_empty()


def test_given_two_deck_containing_same_card_then_are_equal():
    deck1 = Deck([Card(Suit.PURPLE, Rank.TWO), Card(Suit.PURPLE, Rank.TWO), Card(Suit.GREEN, Rank.ONE)])
    deck2 = Deck([Card(Suit.PURPLE, Rank.TWO), Card(Suit.PURPLE, Rank.TWO), Card(Suit.GREEN, Rank.ONE)])

    assert deck1 == deck2


def test_given_two_random_deck_then_are_not_equal():
    deck1 = Deck.generate()
    deck2 = Deck.generate()

    assert deck1 != deck2
