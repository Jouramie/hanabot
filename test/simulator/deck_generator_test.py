from typing import List

from simulator.game.card import Suit, Rank, Card
from simulator.game.deckgenerator import DeckGenerator
from test.simulator.game_setup import get_suits


def test_3suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(get_suits(3))


def test_4suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(get_suits(4))


def test_5suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(get_suits(5))


def test_6suits_should_contain_correct_number_of_cards():
    generate_deck_and_assert_number_of_cards_per_suit(get_suits(6))


def test_6suits_should_shuffle_differently_each_time():
    suits = get_suits(6)
    generator = DeckGenerator()
    deck1 = generator.GenerateDeck(suits)
    deck2 = generator.GenerateDeck(suits)
    deck3 = generator.GenerateDeck(suits)
    deck4 = generator.GenerateDeck(suits)
    deck5 = generator.GenerateDeck(suits)

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


def generate_deck_and_assert_number_of_cards_per_suit(suits: List[Suit]):
    generator = DeckGenerator()
    deck = generator.GenerateDeck(suits)
    for suit in suits:
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.ONE) == 3
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.TWO) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.THREE) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.FOUR) == 2
        assert sum(1 for card in deck if card.suit == suit and card.rank == Rank.FIVE) == 1


def decks_are_different(deck1: List[Card], deck2: List[Card]):
    assert len(deck1) == len(deck2)
    for i in range(0, len(deck1)):
        if deck1[i].rank != deck2[i].rank or deck1[i].suit != deck2[i].suit:
            return

    assert 0 == 1
