from typing import List

from core import Deck, Variant, Card, Suit, Rank
from core.state.discard_pile import DiscardPile
from core.state.play_area import PlayArea
from core.state.stack import Stack
from core.state.status import Status
from core.state.gamestate import GameState
from simulator.game.clue import Clue
from simulator.game.hand_card import HandCard
from simulator.game.player import Player
from test.simulator.game.game_setup import get_player_names


def test_create_gamestate_should_save_all_parameters():
    suits = Variant.NO_VARIANT
    players = []
    for playerName in get_player_names(5):
        players.append(Player(playerName))
    deck = Deck.generate(suits)
    discard_pile = DiscardPile()
    play_area = PlayArea(suits)
    status = Status(35)

    gamestate = GameState(players, deck, discard_pile, play_area, status)

    assert_players_are_equivalent(gamestate.players, players)
    assert_deck_is_equivalent(gamestate.deck, deck)
    assert_discard_pile_is_equivalent(gamestate.discard_pile, discard_pile)
    assert_play_area_is_equivalent(gamestate.play_area, play_area)
    assert_status_is_equivalent(gamestate.status, status)


def test_create_gamestate_should_make_copies():
    suits = Variant.NO_VARIANT
    players = []
    for playerName in get_player_names(5):
        players.append(Player(playerName))
    deck = Deck.generate(suits)
    discard_pile = DiscardPile()
    play_area = PlayArea(suits)
    status = Status(35)

    gamestate = GameState(players, deck, discard_pile, play_area, status)

    players.append(Player("fake player"))
    _, card = deck.draw()
    discard_pile.discard(card)
    play_area.stacks[Suit.RED].last_played = Rank.THREE
    status.clues = 4
    status.strikes = 1
    status.turn = 7

    assert len(gamestate.players) == 5
    assert len(gamestate.deck) == 50
    assert len(gamestate.discard_pile.cards) == 0
    assert gamestate.play_area.stacks[Suit.RED].last_played is None
    assert gamestate.status.clues == 8
    assert gamestate.status.strikes == 0
    assert gamestate.status.turn == 0

    assert len(players) == 6
    assert len(deck) == 49
    assert len(discard_pile.cards) == 1
    assert play_area.stacks[Suit.RED].last_played == Rank.THREE
    assert status.clues == 4
    assert status.strikes == 1
    assert status.turn == 7


def test_copy_gamestate_should_make_copies():
    suits = Variant.NO_VARIANT
    players = []
    for playerName in get_player_names(5):
        players.append(Player(playerName))
    deck = Deck.generate(suits)
    discard_pile = DiscardPile()
    play_area = PlayArea(suits)
    status = Status(35)

    gamestate = GameState(players, deck, discard_pile, play_area, status)
    gamestate_copy = GameState.from_gamestate(gamestate)

    gamestate.players.append(Player("fake player"))
    _, card = gamestate.deck.draw()
    gamestate.discard_pile.discard(card)
    gamestate.play_area.stacks[Suit.RED].last_played = Rank.THREE
    gamestate.status.clues = 4
    gamestate.status.strikes = 1
    gamestate.status.turn = 7

    assert len(gamestate_copy.players) == 5
    assert len(gamestate_copy.deck) == 50
    assert len(gamestate_copy.discard_pile.cards) == 0
    assert gamestate_copy.play_area.stacks[Suit.RED].last_played is None
    assert gamestate_copy.status.clues == 8
    assert gamestate_copy.status.strikes == 0
    assert gamestate_copy.status.turn == 0

    assert len(gamestate.players) == 6
    assert len(gamestate.deck) == 49
    assert len(gamestate.discard_pile.cards) == 1
    assert gamestate.play_area.stacks[Suit.RED].last_played == Rank.THREE
    assert gamestate.status.clues == 4
    assert gamestate.status.strikes == 1
    assert gamestate.status.turn == 7


def assert_players_are_equivalent(players1: List[Player], players2: List[Player]):
    assert len(players1) == len(players2)
    for i in range(0, len(players1)):
        assert_player_is_equivalent(players1[i], players2[i])


def assert_player_is_equivalent(player1: Player, player2: Player):
    assert player1.name == player2.name
    assert_hand_is_equivalent(player1.hand, player2.hand)


def assert_hand_is_equivalent(hand1: List[HandCard], hand2: List[HandCard]):
    assert len(hand1) == len(hand2)
    for i in range(0, len(hand1)):
        assert_handcard_is_equivalent(hand1[i], hand2[i])


def assert_handcard_is_equivalent(card1: HandCard, card2: HandCard):
    assert card1.draw_id == card2.draw_id
    assert card1.is_clued == card2.is_clued
    assert card1.suits_in_game == card2.is_clued
    assert_card_is_equivalent(card1.real_card, card2.real_card)

    assert_suits_in_game_are_equivalent(card1.suits_in_game, card2.suits_in_game)
    assert_received_clues_are_equivalent(card1.received_clues, card2.received_clues)
    assert_possible_cards_are_equivalent(card1.possible_cards, card2.possible_cards)


def assert_cards_are_equivalent(cards1: List[Card], cards2: List[Card]):
    assert len(cards1) == len(cards2)
    for i in range(0, len(cards1)):
        assert_card_is_equivalent(cards1[i], cards2[i])


def assert_card_is_equivalent(card1: Card, card2: Card):
    assert card1.rank == card2.rank
    assert card1.suit == card2.suit


def assert_suits_in_game_are_equivalent(suits1: List[Suit], suits2: List[Suit]):
    assert len(suits1) == len(suits2)
    for i in range(0, len(suits1)):
        assert suits1[i] == suits2[i]


def assert_received_clues_are_equivalent(clues1: List[Clue], clues2: List[Clue]):
    assert len(clues1) == len(clues2)
    for i in range(0, len(clues1)):
        assert clues1[i].turn == clues2[i].turn
        assert clues1[i].touched_slots == clues2[i].touched_slots
        assert clues1[i].receiver_name == clues2[i].receiver_name
        assert clues1[i].giver_name == clues2[i].giver_name
        assert clues1[i].touched_draw_ids == clues2[i].touched_draw_ids


def assert_possible_cards_are_equivalent(cards1: List[Card], cards2: List[Card]):
    assert len(cards1) == len(cards2)
    for i in range(0, len(cards1)):
        assert cards1[i] == cards2[i]


def assert_deck_is_equivalent(deck1: Deck, deck2: Deck):
    assert deck1 == deck2


def assert_discard_pile_is_equivalent(discard1: DiscardPile, discard2: DiscardPile):
    assert_cards_are_equivalent(discard1.cards, discard2.cards)


def assert_play_area_is_equivalent(play1: PlayArea, play2: PlayArea):
    assert len(play1.stacks) == len(play2.stacks)
    for suit in play1.stacks:
        stack1 = play1.stacks[suit]
        stack2 = play2.stacks[suit]
        assert_stack_is_equivalent(stack1, stack2)


def assert_stack_is_equivalent(stack1: Stack, stack2: Stack):
    assert stack1.suit == stack2.suit
    assert stack1.last_played == stack2.last_played


def assert_status_is_equivalent(status1: Status, status2: Status):
    assert status1.turn == status2.turn
    assert status1.clues == status2.clues
    assert status1.strikes == status2.strikes
    assert status1.is_over == status2.is_over
    assert status1.turns_remaining == status2.turns_remaining
