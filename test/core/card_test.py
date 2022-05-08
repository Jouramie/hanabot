import pytest

from core import Rank, Variant, Card
from test.simulator.game.game_setup import get_ranks


@pytest.mark.parametrize(
    ["rank_to_play", "already_played_rank", "expected_result"],
    [
        (Rank.ONE, None, True),
        (Rank.ONE, Rank.ONE, False),
        (Rank.ONE, Rank.TWO, False),
        (Rank.ONE, Rank.THREE, False),
        (Rank.ONE, Rank.FOUR, False),
        (Rank.ONE, Rank.FIVE, False),
        (Rank.TWO, None, False),
        (Rank.TWO, Rank.ONE, True),
        (Rank.TWO, Rank.TWO, False),
        (Rank.TWO, Rank.THREE, False),
        (Rank.TWO, Rank.FOUR, False),
        (Rank.TWO, Rank.FIVE, False),
        (Rank.THREE, None, False),
        (Rank.THREE, Rank.ONE, False),
        (Rank.THREE, Rank.TWO, True),
        (Rank.THREE, Rank.THREE, False),
        (Rank.THREE, Rank.FOUR, False),
        (Rank.THREE, Rank.FIVE, False),
        (Rank.FOUR, None, False),
        (Rank.FOUR, Rank.ONE, False),
        (Rank.FOUR, Rank.TWO, False),
        (Rank.FOUR, Rank.THREE, True),
        (Rank.FOUR, Rank.FOUR, False),
        (Rank.FOUR, Rank.FIVE, False),
        (Rank.FIVE, None, False),
        (Rank.FIVE, Rank.ONE, False),
        (Rank.FIVE, Rank.TWO, False),
        (Rank.FIVE, Rank.THREE, False),
        (Rank.FIVE, Rank.FOUR, True),
        (Rank.FIVE, Rank.FIVE, False),
    ],
)
def test_given_ranks_combinations_when_is_playable_over_then_is_only_playable_over_one_rank_lower_ranks(rank_to_play, already_played_rank, expected_result):
    assert rank_to_play.is_playable_over(already_played_rank) is expected_result


@pytest.mark.parametrize("suit", [suit for suit in Variant.NO_VARIANT])
@pytest.mark.parametrize("rank", [rank for rank in get_ranks()])
def test_create_card_should_create_correct_card(suit, rank):
    card = Card.create(suit, rank)

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

    card1 = Card.create(suit1, rank1)
    card2 = Card.create(suit2, rank2)

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
    card1 = Card.create(suit, rank)
    card2 = Card.create(suit, rank)

    assert id(card1) == id(card2)


@pytest.mark.parametrize("suit1", [suit1 for suit1 in Variant.NO_VARIANT])
@pytest.mark.parametrize("suit2", [suit2 for suit2 in Variant.NO_VARIANT])
@pytest.mark.parametrize("rank1", [rank1 for rank1 in get_ranks()])
@pytest.mark.parametrize("rank2", [rank2 for rank2 in get_ranks()])
def test_get_two_different_cards_twice_should_create_two_and_provide_four_times(suit1, suit2, rank1, rank2):
    if suit1 == suit2 and rank1 == rank2:
        return

    card1 = Card.create(suit1, rank1)
    card2 = Card.create(suit2, rank2)
    card3 = Card.create(suit2, rank2)
    card4 = Card.create(suit1, rank1)

    assert id(card1) != id(card2)
    assert id(card1) != id(card3)
    assert id(card1) == id(card4)
    assert id(card2) == id(card3)
    assert id(card2) != id(card4)
    assert id(card3) != id(card4)


@pytest.mark.parametrize("suit", [suit for suit in Variant.NO_VARIANT])
@pytest.mark.parametrize("rank", [rank for rank in get_ranks()])
def test_get_card_twice_from_different_factory_should_create_one_card_and_provide_it_twice(suit, rank):
    card1 = Card.create(suit, rank)
    card2 = Card.create(suit, rank)

    assert id(card1) == id(card2)