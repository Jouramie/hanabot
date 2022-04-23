from bots.domain.decision import RankClueDecision, PlayDecision
from bots.domain.model.game_state import GameHistory
from bots.domain.model.player import create_unknown_hand, create_unknown_real_hand, PlayerHand, PlayerCard, create_unknown_card
from bots.hanabot.convention import Conventions
from bots.hanabot.conventions import basic
from bots.hanabot.hanabot import Hanabot
from core.card import Card, Suit, Rank, all_possible_cards
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


suits = (Suit.BLUE, Suit.GREEN, Suit.YELLOW, Suit.RED, Suit.PURPLE)
deck = (
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
)


def test_given_first_turn_when_play_turn_then_clue_one():
    hanabot = Hanabot("Alice", Conventions(basic))
    game_state = (
        RelativeGameStateBuilder(suits)
        .set_my_hand(create_unknown_hand("Alice"))
        .set_other_player_hands(
            (
                create_unknown_real_hand(
                    "Bob",
                    [
                        Card(Suit.RED, Rank.ONE),
                        Card(Suit.PURPLE, Rank.TWO),
                        Card(Suit.PURPLE, Rank.THREE),
                        Card(Suit.PURPLE, Rank.FOUR),
                        Card(Suit.PURPLE, Rank.FIVE),
                    ],
                ),
                create_unknown_real_hand(
                    "Cathy",
                    [
                        Card(Suit.BLUE, Rank.TWO),
                        Card(Suit.GREEN, Rank.FOUR),
                        Card(Suit.YELLOW, Rank.FIVE),
                        Card(Suit.RED, Rank.TWO),
                        Card(Suit.PURPLE, Rank.THREE),
                    ],
                ),
            )
        )
        .build()
    )

    decision = hanabot.play_turn(game_state, GameHistory())

    assert decision == RankClueDecision(Rank.ONE, 0)


def test_given_second_turn_when_play_turn_then_clue_one():
    hanabot = Hanabot("Bob", Conventions(basic))
    game_state = (
        RelativeGameStateBuilder(suits)
        .set_my_hand(
            PlayerHand(
                "Bob",
                (
                    PlayerCard(all_possible_cards(suits=suits, ranks=(Rank.ONE,)), True, 0),
                    create_unknown_card(),
                    create_unknown_card(),
                    create_unknown_card(),
                    create_unknown_card(),
                ),
            )
        )
        .set_other_player_hands(
            (
                create_unknown_real_hand(
                    "Cathy",
                    [
                        Card(Suit.BLUE, Rank.TWO),
                        Card(Suit.GREEN, Rank.FOUR),
                        Card(Suit.YELLOW, Rank.FIVE),
                        Card(Suit.RED, Rank.TWO),
                        Card(Suit.PURPLE, Rank.THREE),
                    ],
                ),
                create_unknown_real_hand(
                    "Alice",
                    [
                        Card(Suit.GREEN, Rank.ONE),
                        Card(Suit.PURPLE, Rank.TWO),
                        Card(Suit.YELLOW, Rank.THREE),
                        Card(Suit.PURPLE, Rank.ONE),
                        Card(Suit.GREEN, Rank.FIVE),
                    ],
                ),
            )
        )
        .build()
    )

    decision = hanabot.play_turn(game_state, GameHistory())

    assert decision == PlayDecision(0)
