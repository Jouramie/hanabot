from typing import Iterable

from core import Deck
from core.card import Rank, Variant, Suit
from simulator.game.deckgenerator import DeckGenerator
from test.simulator.game_setup import get_suits


def test_3suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(Variant.THREE_SUITS)


def test_4suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(Variant.FOUR_SUITS)


def test_5suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(Variant.NO_VARIANT)


def test_6suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(Variant.SIX_SUITS)


def test_6suits_should_shuffle_differently_each_time():
    suits = get_suits(6)
    generator = DeckGenerator()
    deck1 = generator.generate_deck(suits)
    deck2 = generator.generate_deck(suits)
    deck3 = generator.generate_deck(suits)
    deck4 = generator.generate_deck(suits)
    deck5 = generator.generate_deck(suits)

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
    generator = DeckGenerator()
    deck = generator.generate_deck(suits)
    for suit in suits:
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.ONE) == 3
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.TWO) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.THREE) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.FOUR) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.FIVE) == 1


def decks_are_different(deck1: Deck, deck2: Deck):
    assert len(deck1) == len(deck2)
    assert deck1 != deck2
