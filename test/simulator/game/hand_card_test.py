import pytest

from core.card import Card
from simulator.game.clue import ColorClue, RankClue
from simulator.game.hand_card import HandCard
from test.simulator.game.game_setup import get_suits, get_possible_cards, get_ranks


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_new_hand_card_should_have_no_clues(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    assert len(hand_card.received_clues) == 0


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_new_hand_card_should_have_correct_card(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    assert hand_card.real_card.suit == card.suit
    assert hand_card.real_card.rank == card.rank


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_new_hand_card_should_remember_game_suits(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    assert hand_card.suits_in_game == suits


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_new_hand_card_should_possibly_be_all_cards(card: Card):
    all_cards = get_possible_cards(get_suits(5))
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    possible_cards = hand_card.get_all_possible_cards()
    assert len(possible_cards) == len(all_cards)
    for card in all_cards:
        assert possible_cards.index(card) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_new_hand_card_should_possibly_be_all_suits(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    possible_suits = hand_card.get_all_possible_suits()
    assert len(possible_suits) == len(suits)
    for suit in suits:
        assert possible_suits.index(suit) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_new_hand_card_should_possibly_be_all_ranks(card: Card):
    suits = get_suits(5)
    ranks = get_ranks()
    hand_card = HandCard(0, card, suits)
    possible_ranks = hand_card.get_all_possible_ranks()
    assert len(possible_ranks) == len(ranks)
    for rank in ranks:
        assert possible_ranks.index(rank) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_color_clued_should_possibly_be_all_cards_of_own_suit(card: Card):
    all_cards_of_own_suit = get_possible_cards([card.suit])
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(card.suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_cards = hand_card.get_all_possible_cards()
    assert len(possible_cards) == len(all_cards_of_own_suit)
    for card in all_cards_of_own_suit:
        assert possible_cards.index(card) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_color_clued_should_possibly_be_only_own_suit(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(card.suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_suits = hand_card.get_all_possible_suits()
    assert len(possible_suits) == 1
    assert possible_suits[0] == card.suit


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_color_clued_should_possibly_be_all_ranks(card: Card):
    suits = get_suits(5)
    ranks = get_ranks()
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(card.suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_ranks = hand_card.get_all_possible_ranks()
    assert len(possible_ranks) == len(ranks)
    for rank in ranks:
        assert possible_ranks.index(rank) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_color_clued_should_possibly_be_all_cards_except_clue_suit(card: Card):
    suits = get_suits(5)
    clue_suit = suits[0]
    if clue_suit == card.suit:
        clue_suit = suits[1]

    suits_other_than_clue_suit = tuple(suit for suit in suits if suit is not clue_suit)

    all_cards_of_other_suits = get_possible_cards(suits_other_than_clue_suit)
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(clue_suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_cards = hand_card.get_all_possible_cards()
    assert len(possible_cards) == len(all_cards_of_other_suits)
    for card in all_cards_of_other_suits:
        assert possible_cards.index(card) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_color_clued_should_possibly_be_not_own_suit(card: Card):
    suits = get_suits(5)
    clue_suit = suits[0]
    if clue_suit == card.suit:
        clue_suit = suits[1]

    suits_other_than_clue_suit = tuple(suit for suit in suits if suit is not clue_suit)

    hand_card = HandCard(0, card, suits)
    clue = ColorClue(clue_suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_suits = hand_card.get_all_possible_suits()
    assert len(possible_suits) == len(suits_other_than_clue_suit)
    for suit in suits_other_than_clue_suit:
        assert possible_suits.index(suit) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_color_clued_should_possibly_be_all_ranks(card: Card):
    suits = get_suits(5)
    clue_suit = suits[0]
    if clue_suit == card.suit:
        clue_suit = suits[1]

    ranks = get_ranks()
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(clue_suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_ranks = hand_card.get_all_possible_ranks()
    assert len(possible_ranks) == len(ranks)
    for rank in ranks:
        assert possible_ranks.index(rank) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_rank_clued_should_possibly_be_all_cards_of_own_rank(card: Card):
    suits = get_suits(5)
    all_cards_of_own_rank = [pcard for pcard in get_possible_cards(suits) if pcard.rank == card.rank]
    hand_card = HandCard(0, card, suits)
    clue = RankClue(card.rank, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_cards = hand_card.get_all_possible_cards()
    assert len(possible_cards) == len(all_cards_of_own_rank)
    for card in all_cards_of_own_rank:
        assert possible_cards.index(card) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_rank_clued_should_possibly_be_only_own_rank(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue = RankClue(card.rank, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_ranks = hand_card.get_all_possible_ranks()
    assert len(possible_ranks) == 1
    assert possible_ranks[0] == card.rank


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_rank_clued_should_possibly_be_all_suits(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue = RankClue(card.rank, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_suits = hand_card.get_all_possible_suits()
    assert len(possible_suits) == len(suits)
    for suit in suits:
        assert possible_suits.index(suit) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_rank_clued_should_possibly_be_all_cards_except_clue_rank(card: Card):
    suits = get_suits(5)
    ranks = get_ranks()
    clue_rank = ranks[0]
    if clue_rank == card.rank:
        clue_rank = ranks[1]

    all_cards_of_other_ranks = [pcard for pcard in get_possible_cards(suits) if pcard.rank != clue_rank]
    hand_card = HandCard(0, card, suits)
    clue = RankClue(clue_rank, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_cards = hand_card.get_all_possible_cards()
    assert len(possible_cards) == len(all_cards_of_other_ranks)
    for card in all_cards_of_other_ranks:
        assert possible_cards.index(card) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_rank_clued_should_possibly_be_not_own_rank(card: Card):
    suits = get_suits(5)
    ranks = get_ranks()
    clue_rank = ranks[0]
    if clue_rank == card.rank:
        clue_rank = ranks[1]

    ranks_other_than_clue_rank = tuple(rank for rank in ranks if rank is not clue_rank)

    hand_card = HandCard(0, card, suits)
    clue = RankClue(clue_rank, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_ranks = hand_card.get_all_possible_ranks()
    assert len(possible_ranks) == len(ranks_other_than_clue_rank)
    for suit in ranks_other_than_clue_rank:
        assert possible_ranks.index(suit) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_rank_clued_should_possibly_be_all_suits(card: Card):
    suits = get_suits(5)
    ranks = get_ranks()
    clue_rank = ranks[0]
    if clue_rank == card.rank:
        clue_rank = ranks[1]

    hand_card = HandCard(0, card, suits)
    clue = RankClue(clue_rank, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    possible_suits = hand_card.get_all_possible_suits()
    assert len(possible_suits) == len(suits)
    for suit in suits:
        assert possible_suits.index(suit) > -1


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_clued_should_remember_clue(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(card.suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    received_clues = hand_card.received_clues
    assert len(received_clues) == 1
    assert received_clues[0] == clue


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_clued_twice_should_remember_both_clue(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue1 = ColorClue(card.suit, "player1", "player0", 1)
    clue2 = RankClue(card.rank, "player1", "player0", 1)
    hand_card.receive_clue(clue1)
    hand_card.receive_clue(clue2)
    received_clues = hand_card.received_clues
    assert len(received_clues) == 2
    assert received_clues[0] == clue1
    assert received_clues[1] == clue2


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_clued_should_be_clued(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(card.suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    assert hand_card.is_clued


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_clued_twice_should_be_clued(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue1 = ColorClue(card.suit, "player1", "player0", 1)
    clue2 = RankClue(card.rank, "player1", "player0", 1)
    hand_card.receive_clue(clue1)
    hand_card.receive_clue(clue2)
    assert hand_card.is_clued


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_clued_should_not_be_clued(card: Card):
    suits = get_suits(5)
    clue_suit = suits[0]
    if clue_suit == card.suit:
        clue_suit = suits[1]
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(clue_suit, "player1", "player0", 1)
    hand_card.receive_clue(clue)
    assert not hand_card.is_clued


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_clued_twice_should_not_be_clued(card: Card):
    suits = get_suits(5)
    clue_suit = suits[0]
    if clue_suit == card.suit:
        clue_suit = suits[1]

    ranks = get_ranks()
    clue_rank = ranks[0]
    if clue_rank == card.rank:
        clue_rank = ranks[1]

    hand_card = HandCard(0, card, suits)
    clue1 = ColorClue(clue_suit, "player1", "player0", 1)
    clue2 = RankClue(clue_rank, "player1", "player0", 1)
    hand_card.receive_clue(clue1)
    hand_card.receive_clue(clue2)
    assert not hand_card.is_clued


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_clued_should_return_true(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(card.suit, "player1", "player0", 1)
    assert hand_card.receive_clue(clue)


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_clued_twice_should_return_true_both_times(card: Card):
    suits = get_suits(5)
    hand_card = HandCard(0, card, suits)
    clue1 = ColorClue(card.suit, "player1", "player0", 1)
    clue2 = RankClue(card.rank, "player1", "player0", 1)
    assert hand_card.receive_clue(clue1)
    assert hand_card.receive_clue(clue2)


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_clued_should_return_false(card: Card):
    suits = get_suits(5)
    clue_suit = suits[0]
    if clue_suit == card.suit:
        clue_suit = suits[1]
    hand_card = HandCard(0, card, suits)
    clue = ColorClue(clue_suit, "player1", "player0", 1)
    assert not hand_card.receive_clue(clue)


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_negative_clued_twice_should_return_false_both_times(card: Card):
    suits = get_suits(5)
    clue_suit = suits[0]
    if clue_suit == card.suit:
        clue_suit = suits[1]

    ranks = get_ranks()
    clue_rank = ranks[0]
    if clue_rank == card.rank:
        clue_rank = ranks[1]

    hand_card = HandCard(0, card, suits)
    clue1 = ColorClue(clue_suit, "player1", "player0", 1)
    clue2 = RankClue(clue_rank, "player1", "player0", 1)
    assert not hand_card.receive_clue(clue1)
    assert not hand_card.receive_clue(clue2)


@pytest.mark.parametrize("card", get_possible_cards(get_suits(5)))
def test_hand_card_clued_four_times_should_return_correct_boolean_every_time(card: Card):
    suits = get_suits(5)
    clue_suit = suits[0]
    if clue_suit == card.suit:
        clue_suit = suits[1]

    ranks = get_ranks()
    clue_rank = ranks[0]
    if clue_rank == card.rank:
        clue_rank = ranks[1]

    hand_card = HandCard(0, card, suits)
    clue1 = ColorClue(clue_suit, "player1", "player0", 1)
    clue2 = ColorClue(card.suit, "player1", "player0", 1)
    clue3 = RankClue(card.rank, "player1", "player0", 1)
    clue4 = RankClue(clue_rank, "player1", "player0", 1)
    assert not hand_card.receive_clue(clue1)
    assert hand_card.receive_clue(clue2)
    assert hand_card.receive_clue(clue3)
    assert not hand_card.receive_clue(clue4)
