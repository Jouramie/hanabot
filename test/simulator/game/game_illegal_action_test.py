import pytest

from core import Deck, Suit, Rank
from simulator.game.action import ColorClueAction, RankClueAction, DiscardAction, PlayAction
from simulator.game.game import Game
from simulator.game.player import Player
from test.simulator.game.game_setup import get_player_names, get_ranks, get_suits


@pytest.mark.parametrize("suit", [suit for suit in get_suits(5)])
def test_give_color_clue_at_0_clues(suit):
    game = Game(get_player_names(5), Deck.generate())
    game.status.clues = 0

    clue = ColorClueAction(suit, game.players[1])

    with pytest.raises(ValueError):
        game.play_turn(clue)


@pytest.mark.parametrize("rank", [rank for rank in get_ranks()])
def test_give_rank_clue_at_0_clues(rank):
    game = Game(get_player_names(5), Deck.generate())
    game.status.clues = 0

    clue = RankClueAction(rank, game.players[1])

    with pytest.raises(ValueError):
        game.play_turn(clue)


def test_give_empty_color_clue():
    game = Game(get_player_names(5), Deck.generate())
    chosen_suit = Suit.RED
    chosen_player = -1
    for i in range(1, len(game.players)):
        suits = list(get_suits(5))
        for card in game.players[i].hand:
            if suits.count(card.real_card.suit) > 0:
                suits.remove(card.real_card.suit)
        if len(suits) > 0:
            chosen_suit = suits[0]
            chosen_player = i
            break

    clue = ColorClueAction(chosen_suit, game.players[chosen_player])

    with pytest.raises(ValueError):
        game.play_turn(clue)


def test_give_empty_rank_clue():
    game = Game(get_player_names(5), Deck.generate())
    chosen_rank = Rank.ONE
    chosen_player = -1
    for i in range(1, len(game.players)):
        ranks = list(get_ranks())
        for card in game.players[i].hand:
            if ranks.count(card.real_card.rank) > 0:
                ranks.remove(card.real_card.rank)
        if len(ranks) > 0:
            chosen_rank = ranks[0]
            chosen_player = i
            break

    clue = RankClueAction(chosen_rank, game.players[chosen_player])

    with pytest.raises(ValueError):
        game.play_turn(clue)


@pytest.mark.parametrize("suit", [suit for suit in get_suits(5)])
def test_give_color_clue_to_self(suit):
    game = Game(get_player_names(5), Deck.generate())

    clue = ColorClueAction(suit, game.players[0])

    with pytest.raises(ValueError):
        game.play_turn(clue)


@pytest.mark.parametrize("rank", [rank for rank in get_ranks()])
def test_give_rank_clue_to_self(rank):
    game = Game(get_player_names(5), Deck.generate())

    clue = RankClueAction(rank, game.players[0])

    with pytest.raises(ValueError):
        game.play_turn(clue)


@pytest.mark.parametrize("suit", [suit for suit in get_suits(5)])
def test_give_color_clue_to_non_existing_player(suit):
    game = Game(get_player_names(5), Deck.generate())

    clue = ColorClueAction(suit, Player("ghost"))

    with pytest.raises(ValueError):
        game.play_turn(clue)


@pytest.mark.parametrize("rank", [rank for rank in get_ranks()])
def test_give_rank_clue_to_non_existing_player(rank):
    game = Game(get_player_names(5), Deck.generate())

    clue = RankClueAction(rank, Player("ghost"))

    with pytest.raises(ValueError):
        game.play_turn(clue)


def test_give_color_clue_on_a_suit_not_in_the_game():
    game = Game(get_player_names(5), Deck.generate())

    clue = ColorClueAction(Suit.TEAL, game.players[1])

    with pytest.raises(ValueError):
        game.play_turn(clue)


@pytest.mark.parametrize("slot", [slot for slot in range(0, 5)])
def test_discard_at_8_clues(slot):
    game = Game(get_player_names(5), Deck.generate())
    game.status.clues = 8

    discard = DiscardAction(slot)

    with pytest.raises(ValueError):
        game.play_turn(discard)


def test_discard_slot_too_low():
    game = Game(get_player_names(5), Deck.generate())
    game.status.clues = 4

    discard = DiscardAction(-1)

    with pytest.raises(ValueError):
        game.play_turn(discard)


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_discard_slot_too_high(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    game.status.clues = 4

    slot = len(game.players[0].hand)

    discard = DiscardAction(slot)

    with pytest.raises(ValueError):
        game.play_turn(discard)


def test_play_slot_too_low():
    game = Game(get_player_names(5), Deck.generate())
    game.status.clues = 4

    play = PlayAction(-1)

    with pytest.raises(ValueError):
        game.play_turn(play)


@pytest.mark.parametrize("number_players", [number_players for number_players in range(2, 7)])
def test_play_slot_too_high(number_players):
    game = Game(get_player_names(number_players), Deck.generate())
    game.status.clues = 4

    slot = len(game.players[0].hand)

    play = PlayAction(slot)

    with pytest.raises(ValueError):
        game.play_turn(play)
