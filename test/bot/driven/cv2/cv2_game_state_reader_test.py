import os

import cv2
import pytest

from bot.domain.card import Suit, Rank, Card
from bot.driven.cv2.cv2_game_state_reader import _read_card_rank, LazyImage, _read_all_cards_for_suit


@pytest.mark.parametrize("card", [card for card in os.listdir("resources/cards") if card[1] is not "0"])
def test_all_card_rank(card):
    card_image = cv2.imread("resources/cards/" + card)
    suit = Suit.from_char(card[0])

    rank = _read_card_rank(LazyImage(card_image), suit)

    assert rank == Rank.from_char(card[1])


@pytest.mark.skip("TODO: fix this test")
def test_read_all_cards_in_first_turn_my_turn():
    screenshot = cv2.imread("resources/screenshots/first-turn-my-turn.png")

    cards = _read_all_cards_for_suit(LazyImage(screenshot), Suit.BLUE)
    cards = [card.card for card in cards]

    assert cards == {
        Card(Suit.BLUE, Rank.ONE),
        Card(Suit.BLUE, Rank.FOUR),
    }
