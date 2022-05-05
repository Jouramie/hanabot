import logging

from bots.hanabot.conventions import level_one
from bots.hanabot.hanabot import Hanabot
from bots.ui.simulator import SimulatorBot
from core import Deck
from core.card import Card, Suit, Rank, Variant
from simulator.controller import Controller
from simulator.game.gamestate import GameState

logging.basicConfig(level=logging.DEBUG)


def test_given_first_turn_when_play_turn_then_clue_and_play_ones():
    deck = Deck.from_starting_hands(
        [
            [
                Card(Suit.GREEN, Rank.ONE),
                Card(Suit.RED, Rank.TWO),
                Card(Suit.YELLOW, Rank.THREE),
                Card(Suit.PURPLE, Rank.ONE),
                Card(Suit.GREEN, Rank.FIVE),
            ],
            [
                Card(Suit.RED, Rank.ONE),
                Card(Suit.PURPLE, Rank.TWO),
                Card(Suit.PURPLE, Rank.THREE),
                Card(Suit.PURPLE, Rank.FOUR),
                Card(Suit.PURPLE, Rank.FIVE),
            ],
            [
                Card(Suit.BLUE, Rank.TWO),
                Card(Suit.GREEN, Rank.FOUR),
                Card(Suit.YELLOW, Rank.FIVE),
                Card(Suit.PURPLE, Rank.TWO),
                Card(Suit.PURPLE, Rank.THREE),
            ],
        ],
        Variant.NO_VARIANT,
    )

    alice = SimulatorBot("alice", Hanabot(level_one))
    bob = SimulatorBot("bob", Hanabot(level_one))
    cathy = SimulatorBot("cathy", Hanabot(level_one))

    controller = Controller()
    game_state = GameState(["alice", "bob", "cathy"], deck)
    controller.resume_game([alice, bob, cathy], game_state)
    controller.current_game.deck = deck

    controller.play_turn()
    controller.play_turn()
    controller.play_turn()
    controller.play_turn()

    assert controller.current_game.play_area.stacks[Suit.RED].last_played == Rank.TWO
