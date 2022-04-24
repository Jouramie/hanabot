from typing import Iterable

from core import Card, Rank, Suit, Variant
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


def test_when_generate_deck_with_starting_hands_then_cards_are_drawn_starting_from_oldest():
    expected_first = Card(Suit.GREEN, Rank.ONE)
    expected_second = Card(Suit.BLUE, Rank.FOUR)
    expected_third = Card(Suit.PURPLE, Rank.TWO)
    expected_fourth = Card(Suit.YELLOW, Rank.ONE)
    expected_fifth = Card(Suit.PURPLE, Rank.TWO)
    expected_sixth = Card(Suit.RED, Rank.FIVE)
    deck = Deck.from_starting_hands(
        [
            [expected_fifth, expected_third, expected_first],
            [expected_sixth, expected_fourth, expected_second],
        ]
    )

    assert expected_first == deck.draw()
    assert expected_second == deck.draw()
    assert expected_third == deck.draw()
    assert expected_fourth == deck.draw()
    assert expected_fifth == deck.draw()
    assert expected_sixth == deck.draw()


def test_3suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(Variant.THREE_SUITS)


def test_4suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(Variant.FOUR_SUITS)


def test_5suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(Variant.NO_VARIANT)


def test_6suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(Variant.SIX_SUITS)


def test_6suits_should_shuffle_differently_each_time():
    variant = Variant.get_suits(6)
    deck1 = Deck.generate(variant)
    deck2 = Deck.generate(variant)
    deck3 = Deck.generate(variant)
    deck4 = Deck.generate(variant)
    deck5 = Deck.generate(variant)

    decks_are_different(deck1, deck2)
    decks_are_different(deck1, deck3)
    decks_are_different(deck1, deck4)
    decks_are_different(deck1, deck5)
    decks_are_different(deck2, deck3)
    decks_are_different(deck2, deck4)
    decks_are_different(deck2, deck5)
    decks_are_different(deck3, deck4)
    decks_are_different(deck3, deck5)
    decks_are_different(deck4, deck5)


def generate_deck_and_assert_number_of_cards_per_suit(suits: Iterable[Suit]):
    deck = Deck.generate(suits)
    for suit in suits:
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.ONE) == 3
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.TWO) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.THREE) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.FOUR) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.FIVE) == 1


def decks_are_different(deck1: Deck, deck2: Deck):
    assert len(deck1) == len(deck2)
    assert deck1 != deck2
