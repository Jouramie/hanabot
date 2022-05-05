from bots.domain.decision import SuitClueDecision, RankClueDecision, DiscardDecision
from bots.domain.model.action import SuitClueAction
from bots.domain.model.game_state import GameHistory
from bots.domain.model.hand import HandCard, Hand
from bots.hanabot.conventions import level_one
from bots.hanabot.hanabot import Hanabot
from core import Card, Rank, Suit
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


def test_given_clued_one_when_play_turn_then_clue_next():
    game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                ),
            )
        )
        .set_other_player_hands(
            Hand(
                "bob",
                (
                    HandCard.clued_real_card(Card(Suit.RED, Rank.ONE), suit_known=True, draw_id=42),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FOUR)),
                ),
            ),
            Hand(
                "cathy",
                (
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FIVE)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.FIVE)),
                    HandCard.unknown_real_card(Card(Suit.RED, Rank.TWO)),
                ),
            ),
        )
        .set_last_performed_action(SuitClueAction("bob", frozenset({0}), frozenset({42}), Suit.RED))
        .build()
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(game_state, GameHistory([game_state]))

    assert decision == SuitClueDecision(Suit.RED, 2)


def test_given_clued_one_when_play_turn_then_clue_another_one():
    game_state = (
        RelativeGameStateBuilder()
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                ),
            )
        )
        .set_other_player_hands(
            Hand(
                "bob",
                (
                    HandCard.clued_real_card(Card(Suit.RED, Rank.ONE), suit_known=True, draw_id=42),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.RED, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FOUR)),
                ),
            ),
            Hand(
                "cathy",
                (
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FIVE)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.FIVE)),
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.ONE)),
                ),
            ),
        )
        .set_last_performed_action(SuitClueAction("bob", frozenset({0}), frozenset({42}), Suit.RED))
        .build()
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(game_state, GameHistory([game_state]))

    assert decision == RankClueDecision(Rank.ONE, 2)


def test_given_all_playable_already_clued_when_play_turn_then_discard():
    game_state = (
        RelativeGameStateBuilder()
        .set_clue_count(4)
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                ),
            )
        )
        .set_other_player_hands(
            Hand(
                "bob",
                (
                    HandCard.clued_real_card(Card(Suit.RED, Rank.ONE), suit_known=True, draw_id=42),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.RED, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FOUR)),
                ),
            ),
            Hand(
                "cathy",
                (
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FIVE)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.FIVE)),
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.TWO)),
                ),
            ),
        )
        .set_last_performed_action(SuitClueAction("bob", frozenset({0}), frozenset({42}), Suit.RED))
        .build()
    )

    alice = Hanabot(level_one)
    decision = alice.play_turn(game_state, GameHistory([game_state]))

    assert decision == DiscardDecision(4)


def test_given_card_already_prompted_when_play_turn_then_do_not_prompt_again():
    game_state = (
        RelativeGameStateBuilder()
        .set_clue_count(5)
        .set_my_hand(
            Hand(
                "donald",
                (
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                    HandCard.unknown_card(),
                ),
            )
        )
        .set_other_player_hands(
            Hand(
                "alice",
                (
                    HandCard.unknown_real_card(Card(Suit.GREEN, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.BLUE, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.GREEN, Rank.TWO)),
                    HandCard.clued_real_card(Card(Suit.PURPLE, Rank.ONE), suit_known=True, draw_id=42),
                ),
            ),
            Hand(
                "cathy",
                (
                    HandCard.clued_real_card(Card(Suit.PURPLE, Rank.TWO), suit_known=True, draw_id=43),
                    HandCard.unknown_real_card(Card(Suit.RED, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.RED, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FOUR)),
                ),
            ),
            Hand(
                "bob",
                (
                    HandCard.unknown_real_card(Card(Suit.YELLOW, Rank.FOUR)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.ONE)),
                    HandCard.unknown_real_card(Card(Suit.PURPLE, Rank.TWO), draw_id=44),
                ),
            ),
        )
        .set_last_performed_action(SuitClueAction("cathy", frozenset({0}), frozenset({43}), Suit.PURPLE))
        .build()
    )

    donald = Hanabot(level_one)
    decision = donald.play_turn(
        game_state,
        GameHistory(
            [
                RelativeGameStateBuilder().set_last_performed_action(SuitClueAction("alice", frozenset({3}), frozenset({42}), Suit.PURPLE)).build(),
                game_state,
            ]
        ),
    )

    assert decision == DiscardDecision(3)
