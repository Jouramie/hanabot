import time

import pytest

from core import Variant, Card
from core.card_factory import CardFactory
from test.simulator.game.game_setup import get_ranks


@pytest.mark.parametrize("suit", [suit for suit in Variant.NO_VARIANT])
@pytest.mark.parametrize("rank", [rank for rank in get_ranks()])
def test_get_card_should_create_correct_card(suit, rank):
    card_factory = CardFactory()

    card = card_factory.get_card(suit, rank)

    assert card is not None
    assert card.suit == suit
    assert card.rank == rank


@pytest.mark.parametrize("suit1", [suit1 for suit1 in Variant.NO_VARIANT])
@pytest.mark.parametrize("suit2", [suit2 for suit2 in Variant.NO_VARIANT])
@pytest.mark.parametrize("rank1", [rank1 for rank1 in get_ranks()])
@pytest.mark.parametrize("rank2", [rank2 for rank2 in get_ranks()])
def test_get_two_different_cards_should_provide_different_cards(suit1, suit2, rank1, rank2):
    if suit1 == suit2 and rank1 == rank2:
        return

    card_factory = CardFactory()

    card1 = card_factory.get_card(suit1, rank1)
    card2 = card_factory.get_card(suit2, rank2)

    assert card1 is not None
    assert card1.suit == suit1
    assert card1.rank == rank1
    assert card2 is not None
    assert card2.suit == suit2
    assert card2.rank == rank2
    assert id(card1) != id(card2)


@pytest.mark.parametrize("suit", [suit for suit in Variant.NO_VARIANT])
@pytest.mark.parametrize("rank", [rank for rank in get_ranks()])
def test_get_card_twice_should_create_one_card_and_provide_it_twice(suit, rank):
    card_factory = CardFactory()

    card1 = card_factory.get_card(suit, rank)
    card2 = card_factory.get_card(suit, rank)

    assert id(card1) == id(card2)


@pytest.mark.parametrize("suit1", [suit1 for suit1 in Variant.NO_VARIANT])
@pytest.mark.parametrize("suit2", [suit2 for suit2 in Variant.NO_VARIANT])
@pytest.mark.parametrize("rank1", [rank1 for rank1 in get_ranks()])
@pytest.mark.parametrize("rank2", [rank2 for rank2 in get_ranks()])
def test_get_two_different_cards_twice_should_create_two_and_provide_four_times(suit1, suit2, rank1, rank2):
    if suit1 == suit2 and rank1 == rank2:
        return

    card_factory = CardFactory()

    card1 = card_factory.get_card(suit1, rank1)
    card2 = card_factory.get_card(suit2, rank2)
    card3 = card_factory.get_card(suit2, rank2)
    card4 = card_factory.get_card(suit1, rank1)

    assert id(card1) != id(card2)
    assert id(card1) != id(card3)
    assert id(card1) == id(card4)
    assert id(card2) == id(card3)
    assert id(card2) != id(card4)
    assert id(card3) != id(card4)


@pytest.mark.parametrize("suit", [suit for suit in Variant.NO_VARIANT])
@pytest.mark.parametrize("rank", [rank for rank in get_ranks()])
def test_get_card_twice_from_different_factory_should_create_one_card_and_provide_it_twice(suit, rank):
    card_factory1 = CardFactory()
    card_factory2 = CardFactory()

    card1 = card_factory1.get_card(suit, rank)
    card2 = card_factory2.get_card(suit, rank)

    assert id(card1) == id(card2)