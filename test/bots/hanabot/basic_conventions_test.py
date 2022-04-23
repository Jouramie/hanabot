from bots.hanabot.convention import Conventions
from bots.hanabot.conventions import basic
from bots.hanabot.hanabot import Hanabot
from bots.ui.simulator import SimulatorBot
from core import Deck
from core.card import Card, Suit, Rank, Variant
from simulator.controller import Controller
from simulator.game.gamestate import GameState

deck = Deck.starting_with(
    [
        Card(Suit.GREEN, Rank.FIVE),
        Card(Suit.PURPLE, Rank.FIVE),
        Card(Suit.PURPLE, Rank.THREE),
        Card(Suit.PURPLE, Rank.ONE),
        Card(Suit.PURPLE, Rank.FOUR),
        Card(Suit.RED, Rank.TWO),
        Card(Suit.YELLOW, Rank.THREE),
        Card(Suit.PURPLE, Rank.THREE),
        Card(Suit.YELLOW, Rank.FIVE),
        Card(Suit.PURPLE, Rank.TWO),
        Card(Suit.PURPLE, Rank.TWO),
        Card(Suit.GREEN, Rank.FOUR),
        Card(Suit.GREEN, Rank.ONE),
        Card(Suit.RED, Rank.ONE),
        Card(Suit.BLUE, Rank.TWO),
    ],
    Variant.NO_VARIANT,
)

alice = SimulatorBot("alice", Hanabot(Conventions(basic)))
bob = SimulatorBot("bob", Hanabot(Conventions(basic)))
cathy = SimulatorBot("cathy", Hanabot(Conventions(basic)))


def test_given_first_turn_when_play_turn_then_clue_one():
    controller = Controller()
    game_state = GameState(["alice", "bob", "cathy"], deck)
    controller.resume_game([alice, bob, cathy], game_state)
    controller.current_game.deck = deck

    controller.play_turn()
    controller.play_turn()

    assert controller.current_game.stacks[Suit.RED].last_played == Rank.ONE
