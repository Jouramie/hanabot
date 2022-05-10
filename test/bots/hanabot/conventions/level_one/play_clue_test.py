from bots.domain.decision import SuitClueDecision
from bots.domain.model.action import SuitClueAction, RankClueAction
from bots.domain.model.game_state import Turn
from bots.domain.model.hand import HandCard, Hand
from bots.hanabot.blackboard import Interpretation, InterpretationType
from bots.hanabot.conventions import PlayClue
from core import Rank, Card, Suit
from core.stack import Stacks
from test.bots.domain.model.game_state_test import RelativeGameStateBuilder


def test_given_one_one_left_to_play_when_find_interpretation_then_only_possible_card_is_one_left_to_play():
    clue = RankClueAction("alice", frozenset({1}), Rank.ONE)
    expected_card = Card(Suit.GREEN, Rank.ONE)

    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.BLUE: Rank.ONE, Suit.RED: Rank.TWO, Suit.YELLOW: Rank.THREE, Suit.PURPLE: Rank.ONE}))
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(1),
                    HandCard.unknown_card(3),
                    HandCard.unknown_card(5),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("bob", 3),
            Hand.create_unknown_hand("cathy", 3),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = PlayClue()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(turn, interpretation_type=InterpretationType.PLAY, explanation=convention.name, notes_on_cards={3: {expected_card}})


def test_given_only_multiple_four_playable_when_find_interpretation_then_only_possible_card_is_playable_four():
    clue = RankClueAction("alice", frozenset({1}), Rank.FOUR)
    expected_cards = {Card(Suit.GREEN, Rank.FOUR), Card(Suit.RED, Rank.FOUR)}

    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.GREEN: Rank.THREE, Suit.RED: Rank.THREE}))
        .set_my_hand(
            Hand(
                "alice",
                (
                    HandCard.unknown_card(1),
                    HandCard.unknown_card(3),
                    HandCard.unknown_card(5),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("bob", 3),
            Hand.create_unknown_hand("cathy", 3),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = PlayClue()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(turn, interpretation_type=InterpretationType.PLAY, explanation=convention.name, notes_on_cards={3: expected_cards})


def test_given_suit_clue_when_find_interpretation_then_find_interpretation():
    clue = SuitClueAction("cathy", frozenset({1}), Suit.BLUE)
    expected_cards = {Card(Suit.BLUE, Rank.THREE)}

    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.BLUE: Rank.TWO}))
        .set_my_hand(
            Hand(
                "cathy",
                (
                    HandCard.unknown_card(1),
                    HandCard.unknown_card(3),
                    HandCard.unknown_card(5),
                ),
            )
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("alice", 3),
            Hand.create_unknown_hand("bob", 3),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = PlayClue()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(turn, interpretation_type=InterpretationType.PLAY, explanation=convention.name, notes_on_cards={3: expected_cards})


def test_given_suit_clue_on_someone_else_when_find_interpretation_then_do_not_find_interpretation():
    clue = SuitClueAction("cathy", frozenset({1}), Suit.BLUE)
    expected_cards = {Card(Suit.BLUE, Rank.THREE)}

    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.BLUE: Rank.TWO}))
        .set_my_hand(
            Hand.create_unknown_hand("alice", 3),
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("bob", 3),
            Hand(
                "cathy",
                (
                    HandCard.unknown_card(1),
                    HandCard.unknown_card(3),
                    HandCard.unknown_card(5),
                ),
            ),
        )
        .build()
    )
    turn = Turn(game_state, clue)

    convention = PlayClue()
    interpretation = convention.find_interpretation(turn)

    assert interpretation == Interpretation(turn, interpretation_type=InterpretationType.PLAY, explanation=convention.name, notes_on_cards={3: expected_cards})


def test_given_card_already_clued_when_find_clue_then_clue_while_touching_clued_card():
    targeted_card = HandCard.unknown_real_card(5, Card(Suit.YELLOW, Rank.ONE))
    game_state = (
        RelativeGameStateBuilder()
        .set_stacks(Stacks.create_from_dict({Suit.BLUE: Rank.ONE}))
        .set_my_hand(
            Hand.create_unknown_hand("alice", 3),
        )
        .set_other_player_hands(
            Hand.create_unknown_hand("bob", 3),
            Hand(
                "cathy",
                (
                    HandCard.unknown_real_card(1, Card(Suit.BLUE, Rank.ONE)),
                    HandCard.clued_real_card(3, Card(Suit.YELLOW, Rank.TWO), rank_known=True),
                    targeted_card,
                ),
            ),
        )
        .build()
    )

    convention = PlayClue()
    decision = convention.find_clue((2, 2, targeted_card), game_state)

    assert decision == [SuitClueDecision(Suit.YELLOW, 2)]
